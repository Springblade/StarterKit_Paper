// Run against a dedicated migrated database and a development server using it.
// pnpm exec vitest run --config vitest.orders.config.ts
import { randomUUID } from 'node:crypto';
import { createRequire } from 'node:module';
import { hashPassword } from 'better-auth/crypto';
import { eq, inArray } from 'drizzle-orm';
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import { db, pool } from '../src/database/db';
import { account, orders, plans, user } from '../src/database/schema';
import { cancelOrder } from '../src/features/billing/actions/cancel-order';
import { checkOrderStatus } from '../src/features/billing/actions/check-order-status';
import { listOrders } from '../src/features/billing/actions/list-orders';

const context = vi.hoisted(() => ({ userId: null as string | null }));
const { JSDOM } = createRequire(import.meta.url)('jsdom') as {
  JSDOM: new (html: string) => { window: { document: Document } };
};
vi.mock('@/features/auth/lib/auth', () => ({
  getSession: async () => context.userId ? { user: { id: context.userId } } : null,
}));
vi.mock('next/cache', () => ({ revalidatePath: vi.fn() }));

const database = new URL(process.env.DATABASE_URL!);
if (!['localhost', '127.0.0.1'].includes(database.hostname) ||
    database.pathname !== '/smartkit_orders_test') {
  throw new Error('Use the dedicated local smartkit_orders_test database only');
}
const base = process.env.TEST_BASE_URL ?? 'http://localhost:3107';
if (!['localhost', '127.0.0.1'].includes(new URL(base).hostname)) {
  throw new Error('HTTP verification must use a local server');
}
const run = randomUUID();
const people = ['a', 'b', 'empty'].map(label => ({
  id: `${run}-${label}`, email: `${run}-${label}@smartkit.local`, name: `Fixture ${label}`,
}));
const states = ['pending', 'completed', 'cancelled', 'expired'] as const;
const planId = `${run}-plan`;
const fixtures = people.slice(0, 2).flatMap(person => states.map((status, index) => ({
  id: `${person.id}-${status}`, code: `${person.id}-${status}`, userId: person.id,
  planId, amountVnd: '99000', status,
  expiresAt: new Date(Date.now() + (status === 'expired' ? -3600000 : 3600000)),
  completedAt: status === 'completed' ? new Date() : null,
  createdAt: new Date(Date.UTC(2026, 0, 1, 0, index)),
})));
const order = (person: number, status: typeof states[number]) =>
  fixtures.find(row => row.userId === people[person]!.id && row.status === status)!;
const cookies: string[] = [];
const password = 'Local-fixture-password-123!';

beforeAll(async () => {
  await db.insert(user).values(people.map(person => ({ ...person, emailVerified: true })));
  const hash = await hashPassword(password);
  await db.insert(account).values(people.map(person => ({
    id: randomUUID(), userId: person.id, accountId: person.id,
    providerId: 'credential' as const, password: hash,
  })));
  await db.insert(plans).values({ id: planId, name: 'Order baseline fixture', priceVnd: '99000' });
  await db.insert(orders).values(fixtures);
  for (const person of people) {
    const response = await fetch(`${base}/api/auth/sign-in/email`, {
      method: 'POST', headers: { 'Content-Type': 'application/json', Origin: base },
      body: JSON.stringify({ email: person.email, password }),
    });
    expect(response.status, 'Real HTTP login must succeed').toBe(200);
    const cookie = response.headers.getSetCookie().map(value => value.split(';')[0]).join('; ');
    expect(cookie).toContain('session_token');
    cookies.push(cookie);
  }
});
beforeEach(() => { context.userId = people[0]!.id; });
afterAll(async () => {
  // Remove only this run's fixtures, even if a check failed.
  try {
    await db.delete(user).where(inArray(user.id, people.map(person => person.id)));
    await db.delete(plans).where(eq(plans.id, planId));
  } finally { await pool.end(); }
});

describe('real HTTP ownership checks', () => {
  for (const person of [0, 1]) {
    it(`user ${person} history includes own codes and excludes the other user's codes`, async () => {
      const response = await fetch(`${base}/dashboard/billing/history`, {
        headers: { Cookie: cookies[person]! }, redirect: 'manual',
      });
      expect(response.status).toBe(200);
      const html = await response.text();
      for (const fixture of fixtures) {
        if (fixture.userId === people[person]!.id) expect(html).toContain(fixture.code);
        else expect(html).not.toContain(fixture.code);
      }
    });
    it(`user ${person} status API enforces ownership for all four states`, async () => {
      for (const fixture of fixtures) {
        const response = await fetch(`${base}/api/orders/${fixture.id}/status`, {
          headers: { Cookie: cookies[person]! }, redirect: 'manual',
        });
        if (fixture.userId === people[person]!.id) {
          expect(response.status).toBe(200);
          expect(await response.json()).toMatchObject({ status: fixture.status });
        } else {
          expect(response.status).toBe(404);
          expect(await response.json()).toEqual({ error: 'Not found' });
        }
      }
    });
  }
  it('anonymous history/status requests do not expose orders', async () => {
    for (const path of ['/dashboard/billing/history', `/api/orders/${fixtures[0]!.id}/status`]) {
      const response = await fetch(`${base}${path}`, { redirect: 'manual' });
      expect([302, 303, 307, 308]).toContain(response.status);
      expect(response.headers.get('location')).toContain('/auth/sign-in');
    }
  });
});

describe('history filter development-task evaluator', () => {
  async function history(person: number, query = '') {
    const response = await fetch(`${base}/dashboard/billing/history${query}`, {
      headers: { Cookie: cookies[person]! }, redirect: 'manual',
    });
    expect(response.status).toBe(200);
    return new JSDOM(await response.text()).window.document;
  }
  function codes(document: Awaited<ReturnType<typeof history>>) {
    return [...document.querySelectorAll('tbody tr')].map(row => row.querySelector('td')?.textContent?.trim());
  }
  it('offers a labelled GET form with all states and preserves selection in the URL', async () => {
    const document = await history(0, '?status=completed');
    const select = document.querySelector<HTMLSelectElement>('select[name="status"]');
    expect(select).not.toBeNull();
    const id = select!.id;
    const label = document.querySelector(`label[for="${id}"]`);
    expect(label?.textContent?.trim()).toBeTruthy();
    const form = select!.closest('form')!;
    expect(form).not.toBeNull();
    expect((form.getAttribute('method') ?? 'get').toLowerCase()).toBe('get');
    expect(form.querySelector('button[type="submit"], input[type="submit"]')).not.toBeNull();
    expect([...select!.querySelectorAll('option')].map(option => option.value).sort())
      .toEqual(['', ...states].sort());
    expect(select!.value).toBe('completed');
    const allUrl = new URL(form.getAttribute('action') || '/dashboard/billing/history', base);
    allUrl.searchParams.set('status', '');
    const reset = await history(0, allUrl.search);
    expect(codes(reset)).toHaveLength(4);
  });
  it('each status shows exactly the owner subset for both users without mutating orders', async () => {
    const before = await db.select().from(orders).where(inArray(orders.id, fixtures.map(row => row.id)));
    for (const person of [0, 1]) {
      for (const status of states) {
        const document = await history(person, `?status=${status}`);
        expect(codes(document), `user ${person} filter ${status}`).toEqual([order(person, status).code]);
        const row = document.querySelector('tbody tr')!;
        expect(row.textContent).toContain('Order baseline fixture');
        expect(row.textContent).toContain('99.000');
        expect(document.querySelector<HTMLSelectElement>('select[name="status"]')?.value).toBe(status);
      }
    }
    const after = await db.select().from(orders).where(inArray(orders.id, fixtures.map(row => row.id)));
    expect(after.sort((a,b) => a.id.localeCompare(b.id))).toEqual(before.sort((a,b) => a.id.localeCompare(b.id)));
  });
  it('missing, empty, invalid and repeated status fall back to full own history in date order', async () => {
    for (const query of ['', '?status=', '?status=unknown', '?status=pending&status=completed']) {
      const document = await history(0, query);
      expect(codes(document)).toEqual([...fixtures.filter(row => row.userId === people[0]!.id)]
        .sort((a,b) => b.createdAt.getTime() - a.createdAt.getTime()).map(row => row.code));
      expect(document.querySelector<HTMLSelectElement>('select[name="status"]')?.value).toBe('');
    }
  });
  it('an empty filtered result retains controls and explains the empty state', async () => {
    const document = await history(2, '?status=pending');
    expect(codes(document)).toEqual([]);
    expect(document.querySelector<HTMLSelectElement>('select[name="status"]')?.value).toBe('pending');
    expect(document.body.textContent).toMatch(/no .*orders|no .*transactions/i);
    const reset = [...document.querySelectorAll('a')].find(link =>
      /all/i.test(link.textContent ?? '') && new URL(link.href, base).pathname === '/dashboard/billing/history');
    expect(reset).toBeTruthy();
  });
  it('anonymous filtered history redirects to sign-in', async () => {
    const response = await fetch(`${base}/dashboard/billing/history?status=completed`, { redirect: 'manual' });
    expect([302,303,307,308]).toContain(response.status);
    expect(response.headers.get('location')).toContain('/auth/sign-in');
  });
});

describe('actual server actions and real SQL; session/cache boundaries stubbed', () => {
  it('rejects anonymous list, status and cancellation', async () => {
    context.userId = null;
    for (const action of [() => listOrders(), () => checkOrderStatus(fixtures[0]!.id),
      () => cancelOrder(fixtures[0]!.id)]) {
      await expect(action()).rejects.toMatchObject({ code: 'UNAUTHORIZED' });
    }
  });
  it('lists only own orders, including when a status filter is supplied', async () => {
    const all = await listOrders();
    expect(all.map(row => row.id).sort()).toEqual(fixtures.filter(row => row.userId === people[0]!.id).map(row => row.id).sort());
    const filtered = await listOrders({ status: 'pending' });
    expect(filtered.map(row => row.id)).toEqual([order(0, 'pending').id]);
  });
  it('status action rejects another owner and nonexistent IDs', async () => {
    await expect(checkOrderStatus(order(1, 'pending').id)).rejects.toMatchObject({ code: 'UNAUTHORIZED' });
    await expect(checkOrderStatus('missing-order')).rejects.toMatchObject({ code: 'ORDER_NOT_FOUND' });
    expect(await checkOrderStatus(order(0, 'completed').id)).toMatchObject({ status: 'completed' });
  });
  it('rejects cancelling foreign, completed, cancelled, expired or missing orders without changing rows', async () => {
    const before = await db.select().from(orders).where(inArray(orders.id, fixtures.map(row => row.id)));
    for (const id of [order(1, 'pending').id, ...states.filter(state => state !== 'pending').map(state => order(0, state).id), 'missing-order']) {
      await expect(cancelOrder(id)).rejects.toMatchObject({ code: 'ORDER_NOT_FOUND_OR_NOT_PENDING' });
    }
    const after = await db.select().from(orders).where(inArray(orders.id, fixtures.map(row => row.id)));
    expect(after.sort((a,b) => a.id.localeCompare(b.id))).toEqual(before.sort((a,b) => a.id.localeCompare(b.id)));
  });
  it('cancels own pending order once and preserves the other user order', async () => {
    const own = order(0, 'pending');
    expect(await cancelOrder(own.id)).toEqual({ orderId: own.id });
    expect(await checkOrderStatus(own.id)).toMatchObject({ status: 'cancelled' });
    await expect(cancelOrder(own.id)).rejects.toMatchObject({ code: 'ORDER_NOT_FOUND_OR_NOT_PENDING' });
    const foreign = await db.query.orders.findFirst({ where: eq(orders.id, order(1, 'pending').id) });
    expect(foreign?.status).toBe('pending');
  });
});
