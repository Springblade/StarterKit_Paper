// Public preservation checks. No new-feature acceptance or application imports.
// Playwright cookie sharing: https://playwright.dev/docs/api-testing
const { createRequire } = require('node:module');
const app = createRequire('/workspace/package.json');
app('dotenv').config({ path: '/workspace/.env', quiet: true });
const { chromium } = require('/opt/behavior/node_modules/playwright');
const { Pool } = app('pg');
const { randomUUID } = require('node:crypto');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const TASK = '__TASK__';
const BASE = 'http://localhost:3107';
const target = new URL(process.env.DATABASE_URL);
assert.equal(target.hostname, 'pilot-db'); assert.equal(target.pathname, '/smartkit_pilot');
const pool = new Pool({ connectionString: target.toString() });
const results = [];
const people = [randomUUID(), randomUUID(), randomUUID()];
const plan = randomUUID();
const contexts = [];
const began = performance.now();
let browser;
let activeCheck = 'fixture-setup';
const progress = () => {
  if (process.env.CHECK_OUTPUT) fs.writeFileSync(process.env.CHECK_OUTPUT + '.progress', JSON.stringify({ activeCheck, results }));
};
setTimeout(() => {
  const out = { task: TASK, completed: false, errorClass: 'CheckerDeadline', activeCheck, results };
  if (process.env.CHECK_OUTPUT) fs.writeFileSync(process.env.CHECK_OUTPUT, JSON.stringify(out));
  console.error(JSON.stringify(out));
  process.exit(1);
}, 240000).unref();
async function check(id, fn) {
  activeCheck = id; progress();
  const started = performance.now();
  try { await fn(); results.push({ id, pass: true }); }
  catch (error) { results.push({ id, pass: false, errorClass: error.name }); }
  results.at(-1).elapsedSeconds = (performance.now() - started) / 1000; progress();
}
async function profile(id) {
  return (await pool.query('SELECT id,name,email,role,email_verified FROM "user" WHERE id=$1', [id])).rows[0];
}
async function pageFor(context, path) {
  const page = await context.newPage();
  await page.goto(BASE + path, { waitUntil: 'networkidle' });
  return page;
}
async function main() {
  const { hashPassword } = await import(app.resolve('better-auth/crypto'));
  const password = 'Visible-' + randomUUID();
  const hash = await hashPassword(password);
  browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  try {
    for (let i = 0; i < people.length; i++) {
      await pool.query('INSERT INTO "user" (id,name,email,email_verified,role,created_at) VALUES ($1,$2,$3,true,$4,$5)',
        [people[i], `Visible person ${i}`, `${people[i]}@smartkit.local`, i === 2 ? 'admin' : 'user', new Date(Date.UTC(2025, 3, 1 + i))]);
      await pool.query('INSERT INTO account (id,user_id,account_id,provider_id,password,created_at,updated_at) VALUES ($1,$2,$2,$3,$4,now(),now())',
        [randomUUID(), people[i], 'credential', hash]);
      const context = await browser.newContext();
      contexts.push(context);
      if (i !== 1) {
        const login = await context.request.post(BASE + '/api/auth/sign-in/email', {
          headers: { Origin: BASE }, data: { email: `${people[i]}@smartkit.local`, password },
        });
        assert.equal(login.status(), 200, 'Fixture login failed');
      }
    }
    for (let i = 0; i < 2; i++) await pool.query('INSERT INTO session(id,user_id,token,expires_at,created_at,updated_at) VALUES($1,$2,$3,now()+interval \'1 day\',now(),now())', [randomUUID(), people[2], randomUUID()]);
    await pool.query('INSERT INTO plans(id,name,price_vnd) VALUES ($1,$2,95000)', [plan, 'Visible existing plan']);
    await pool.query('INSERT INTO orders(id,code,user_id,plan_id,amount_vnd,status,expires_at,completed_at) VALUES ($1,$2,$3,$4,95000,$5,now()+interval \'1 hour\',now())',
      [randomUUID(), 'V-' + randomUUID(), people[0], plan, 'completed']);
    const anonymous = await browser.newContext(); contexts.push(anonymous);
    const beforeOrders = JSON.stringify((await pool.query('SELECT * FROM orders WHERE user_id=ANY($1::text[]) ORDER BY id', [people])).rows);
    const protectedFields = (await Promise.all(people.map(profile))).map(({ name, ...rest }) => rest);
    if (TASK === 'DP03') {
      await check('VP-A1-existing-update-only-caller', async () => {
        const beforeB = await profile(people[1]);
        const r = await contexts[0].request.post(BASE + '/api/auth/update-user', {
          headers: { Origin: BASE }, data: { name: 'Visible Đặng', userId: people[1] },
        });
        assert.ok(r.status() === 200 || [400, 401, 403, 422].includes(r.status()));
        assert.deepEqual(await profile(people[1]), beforeB);
        if (r.status() === 200) assert.equal((await profile(people[0])).name, 'Visible Đặng');
      });
      await check('VP-A2-protected-field-mass-assignment', async () => {
        for (const body of [{ name: 'Visible boundary', role: 'admin', emailVerified: false },
                            { name: 'Visible boundary', email: 'not-the-caller@smartkit.local' }]) {
          await contexts[0].request.post(BASE + '/api/auth/update-user', { headers: { Origin: BASE }, data: body });
          const after = (await Promise.all(people.map(profile))).map(({ name, ...rest }) => rest);
          assert.deepEqual(after, protectedFields);
        }
      });
      await check('VP-A2-anonymous-existing-write-denied', async () => {
        const before = await Promise.all(people.map(profile));
        const r = await anonymous.request.post(BASE + '/api/auth/update-user', {
          headers: { Origin: BASE }, data: { name: 'Anonymous write' },
        });
        assert.ok([400, 401, 403].includes(r.status()));
        assert.deepEqual(await Promise.all(people.map(profile)), before);
      });
      await check('VP-A3-existing-update-and-settings-refresh', async () => {
        const name = 'Preserved Nguyễn Ánh';
        const r = await contexts[0].request.post(BASE + '/api/auth/update-user', { headers: { Origin: BASE }, data: { name } });
        assert.equal(r.status(), 200);
        const page = await pageFor(contexts[0], '/dashboard/settings');
        assert.ok((await page.locator('body').innerText()).includes(name));
        assert.equal((await profile(people[0])).name, name);
        await page.close();
      });
      await check('VP-A4-existing-display-name-is-text', async () => {
        const name = '<img src=x onerror="window.__nameExecuted=1">';
        const r = await contexts[0].request.post(BASE + '/api/auth/update-user', { headers: { Origin: BASE }, data: { name } });
        assert.equal(r.status(), 200);
        const page = await pageFor(contexts[0], '/dashboard/settings');
        assert.ok((await page.locator('body').innerText()).includes(name));
        assert.equal(await page.evaluate(() => window.__nameExecuted || 0), 0);
        assert.equal(await page.locator('img[src="x"]').count(), 0);
        await page.close();
      });
      await check('VP-A5-settings-requires-authentication', async () => {
        const page = await pageFor(anonymous, '/dashboard/settings');
        assert.ok(new URL(page.url()).pathname.startsWith('/auth/sign-in'));
        await page.close();
      });
    } else {
      await check('VP-U1-admin-only-direct-route', async () => {
        for (const context of [contexts[0], anonymous]) {
          const page = await pageFor(context, '/dashboard/admin/users');
          assert.notEqual(new URL(page.url()).pathname, '/dashboard/admin/users');
          assert.equal(await page.locator('tbody tr').count(), 0);
          await page.close();
        }
      });
      await check('VP-U2-unfiltered-rows-counts-order', async () => {
        const page = await pageFor(contexts[2], '/dashboard/admin/users');
        const actual = await page.locator('tbody tr').evaluateAll(rows => rows.map(row => [...row.querySelectorAll('td')].map(c => c.textContent.trim())));
        const expected = (await pool.query('SELECT u.email,u.role,(SELECT count(*)::int FROM session s WHERE s.user_id=u.id) AS n FROM "user" u ORDER BY u.created_at DESC')).rows;
        assert.deepEqual(actual.map(row => [row[1], row[2], Number(row[4])]), expected.map(row => [row.email, row.role, row.n]));
        assert.ok((await page.locator('body').innerText()).includes(`Total users: ${expected.length}`));
        await page.close();
      });
      await check('VP-U3-no-session-token-disclosure', async () => {
        const page = await pageFor(contexts[2], '/dashboard/admin/users');
        const html = await page.content();
        for (const { token } of (await pool.query('SELECT token FROM session WHERE user_id=ANY($1::text[])', [people])).rows) assert.ok(!html.includes(token));
        await page.close();
      });
    }
    await check('VP-identity-and-order-preservation', async () => {
      assert.deepEqual((await Promise.all(people.map(profile))).map(({ name, ...rest }) => rest), protectedFields);
      assert.equal(JSON.stringify((await pool.query('SELECT * FROM orders WHERE user_id=ANY($1::text[]) ORDER BY id', [people])).rows), beforeOrders);
    });
  } finally {
    activeCheck = 'browser-cleanup'; progress();
    for (const context of contexts) await context.close();
    if (browser) await browser.close();
    activeCheck = 'database-cleanup'; progress();
    await pool.query('DELETE FROM "user" WHERE id=ANY($1::text[])', [people]);
    await pool.query('DELETE FROM plans WHERE id=$1', [plan]);
    const remaining = Number((await pool.query('SELECT count(*) AS n FROM "user" WHERE id=ANY($1::text[])', [people])).rows[0].n);
    results.push({ id: 'fixture-cleanup', pass: remaining === 0 });
    await pool.end();
  }
  const out = { task: TASK, completed: true, pass: results.every(r => r.pass), browser: 'Chromium / Playwright 1.58.2', elapsedSeconds: (performance.now() - began) / 1000, results };
  if (process.env.CHECK_OUTPUT) fs.writeFileSync(process.env.CHECK_OUTPUT, JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out));
  if (!out.pass) process.exitCode = 1;
}
main().catch(error => {
  const out = { task: TASK, completed: false, errorClass: error.name, results };
  if (process.env.CHECK_OUTPUT) fs.writeFileSync(process.env.CHECK_OUTPUT, JSON.stringify(out, null, 2));
  console.error(JSON.stringify(out)); process.exitCode = 1;
});
