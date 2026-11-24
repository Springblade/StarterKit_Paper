// Withheld evaluator. Separate sparse fixtures and assertions from visible checks.
const { createRequire } = require('node:module');
const app = createRequire('/workspace/package.json');
app('dotenv').config({ path: '/workspace/.env', quiet: true });
const { chromium } = require('/opt/behavior/node_modules/playwright');
const { Pool } = app('pg');
const { randomUUID } = require('node:crypto');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const TASK = process.env.CHECK_TASK;
const BASE = 'http://localhost:3107';
const database = new URL(process.env.DATABASE_URL);
assert.equal(database.hostname, 'pilot-db'); assert.equal(database.pathname, '/smartkit_pilot');
const pool = new Pool({ connectionString: database.toString() });
const ids = Array.from({ length: 4 }, () => randomUUID());
const plan = randomUUID();
const contexts = [];
const results = [];
const consoleErrors = [];
let browser, anonymous, password, captured;
const began = performance.now();
let activeCheck = 'fixture-setup';
const outputPath = process.env.CHECK_OUTPUT || '/evaluator/final.json';
const progress = () => fs.writeFileSync(outputPath + '.progress', JSON.stringify({ activeCheck, results }));
setTimeout(() => {
  const out = { task: TASK, completed: false, errorClass: 'CheckerDeadline', activeCheck, results };
  fs.writeFileSync(outputPath, JSON.stringify(out));
  console.error(JSON.stringify(out));
  process.exit(1);
}, 240000).unref();
async function check(id, kind, fn) {
  activeCheck = id; progress();
  const started = performance.now();
  try { await fn(); results.push({ id, kind, pass: true }); }
  catch (error) { results.push({ id, kind, pass: false, errorClass: error.name,
    location: error.stack?.split('\n').find(line => line.includes('/evaluator/'))?.trim() }); }
  results.at(-1).elapsedSeconds = (performance.now() - started) / 1000; progress();
}
async function account(id) {
  return (await pool.query('SELECT id,name,email,email_verified,role FROM "user" WHERE id=$1', [id])).rows[0];
}
async function accounts() { return Promise.all(ids.map(account)); }
function protectedPart(rows) { return rows.map(({ name, ...rest }) => rest); }
async function newPage(ctx, path) {
  const page = await ctx.newPage();
  page.on('pageerror', e => consoleErrors.push(e.name));
  await page.goto(BASE + path, { waitUntil: 'networkidle' });
  return page;
}
async function displayed(page) {
  return page.locator('tbody tr').evaluateAll(rows => rows.map(row => [...row.querySelectorAll('td')].map(cell => cell.textContent.trim())));
}
async function roleControl(page) {
  const select = page.locator('select').filter({ has: page.locator('option[value="admin"]') })
    .filter({ has: page.locator('option[value="user"]') });
  assert.equal(await select.count(), 1, 'A native role selector must exist');
  assert.ok(await select.evaluate(element => Boolean(
    element.getAttribute('aria-label')?.trim() || [...(element.labels || [])].some(label => label.textContent.trim()) ||
    (element.getAttribute('aria-labelledby') || '').split(/\s+/).some(id => document.getElementById(id)?.textContent.trim())
  )), 'The role selector must be labelled');
  return select;
}
async function submitName(page, value, tamper) {
  const input = page.getByRole('textbox', { name: /display.*name|^name$|full.*name|tên/i });
  assert.equal(await input.count(), 1, 'A labelled editable display name must exist');
  await input.fill(value);
  if (tamper) {
    await page.route('**/*', async route => {
      const request = route.request();
      let body = request.postData();
      if (request.method() === 'POST' && body && new URL(request.url()).origin === BASE && body.includes(value)) {
        if (tamper.replacement !== undefined) body = body.split(value).join(tamper.replacement);
        if (tamper.foreign) {
          if ((request.headers()['content-type'] || '').includes('application/json')) {
            const data = JSON.parse(body);
            const fields = { userId: ids[2], id: ids[2], role: 'admin', emailVerified: false, email: 'forged@smartkit.local' };
            body = JSON.stringify(Array.isArray(data)
              ? [...data.map(arg => arg && typeof arg === 'object' ? { ...arg, ...fields } : arg), fields]
              : { ...data, ...fields });
          } else {
            const contentType = request.headers()['content-type'] || '';
            const boundary = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/);
            assert.ok(boundary, 'Unsupported action transport for identity tampering');
            const block = body.split('--' + (boundary[1] || boundary[2])).find(part => part.includes(value));
            const field = block?.match(/name="([^"]+)"/);
            assert.ok(field, 'Name field not found in action transport');
            const prefix = field[1].match(/^\d+_/)?.[0] || '';
            const b = boundary[1] || boundary[2];
            const fields = { userId: ids[2], id: ids[2], role: 'admin', emailVerified: 'false', email: 'forged@smartkit.local' };
            const extra = Object.entries(fields).map(([key, value]) => `--${b}\r\nContent-Disposition: form-data; name="${prefix}${key}"\r\n\r\n${value}\r\n`).join('');
            body = body.replace(`--${b}--`, extra + `--${b}--`);
          }
        }
        tamper.seen = true;
        captured = { url: request.url(), method: request.method(), headers: request.headers(), body };
        await route.continue({ postData: body });
      } else await route.continue();
    });
  }
  const post = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).origin === BASE, { timeout: 15000 });
  await input.locator('xpath=ancestor::form').getByRole('button', { name: /save|update|lưu|cập nhật/i }).click();
  await post;
  await page.waitForLoadState('networkidle');
  if (tamper) {
    await page.unroute('**/*');
    assert.equal(tamper.seen, true, 'Actual write transport must be exercised');
  }
}
async function main() {
  const { hashPassword } = await import(app.resolve('better-auth/crypto'));
  password = 'Withheld-' + randomUUID();
  const hash = await hashPassword(password);
  browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  try {
    for (let i = 0; i < ids.length; i++) {
      await pool.query('INSERT INTO "user"(id,name,email,email_verified,role,created_at) VALUES($1,$2,$3,true,$4,$5)',
        [ids[i], `Final account ${i}`, `${ids[i]}@smartkit.local`, i === 0 || i === 3 ? 'admin' : 'user', new Date(Date.UTC(2024, 8, 9 + 3 * i))]);
      await pool.query('INSERT INTO account(id,user_id,account_id,provider_id,password,created_at,updated_at) VALUES($1,$2,$2,$3,$4,now(),now())', [randomUUID(), ids[i], 'credential', hash]);
      const ctx = await browser.newContext(); contexts.push(ctx);
      if (i !== 2) {
        const r = await ctx.request.post(BASE + '/api/auth/sign-in/email', { headers: { Origin: BASE }, data: { email: `${ids[i]}@smartkit.local`, password } });
        assert.equal(r.status(), 200, 'Fixture login');
      }
    }
    // Sparse session distribution differs from the visible package, including 0/1/3 records.
    for (const [i, n] of [[0, 2], [3, 1]]) for (let k = 0; k < n; k++) {
      await pool.query('INSERT INTO session(id,user_id,token,expires_at,created_at,updated_at) VALUES($1,$2,$3,now()+interval \'1 day\',now(),now())', [randomUUID(), ids[i], randomUUID()]);
    }
    await pool.query('INSERT INTO plans(id,name,price_vnd) VALUES($1,$2,137000)', [plan, 'Hidden retained purchase']);
    for (const [i, status] of [[1, 'completed'], [2, 'expired']]) {
      await pool.query('INSERT INTO orders(id,code,user_id,plan_id,amount_vnd,status,expires_at,completed_at) VALUES($1,$2,$3,$4,137000,$5,now()-interval \'1 hour\',$6)', [randomUUID(), 'H-' + randomUUID(), ids[i], plan, status, status === 'completed' ? new Date() : null]);
    }
    anonymous = await browser.newContext(); contexts.push(anonymous);
    const before = await accounts();
    const ordersBefore = JSON.stringify((await pool.query('SELECT * FROM orders WHERE user_id=ANY($1::text[]) ORDER BY id', [ids])).rows);
    if (TASK === 'DP02') {
      await check('U-P1-direct-route-non-admin-and-anonymous', 'preservation', async () => {
        for (const ctx of [contexts[1], anonymous]) {
          const page = await newPage(ctx, '/dashboard/admin/users?role=admin');
          assert.notEqual(new URL(page.url()).pathname, '/dashboard/admin/users');
          assert.equal(await page.locator('tbody tr').count(), 0); await page.close();
        }
      });
      for (const role of ['', 'user', 'admin']) {
        await check('U-A-role-' + (role || 'all'), 'acceptance', async () => {
          const page = await newPage(contexts[0], '/dashboard/admin/users' + (role ? '?role=' + role : ''));
          const select = await roleControl(page);
          assert.equal(await select.count(), 1);
          assert.equal(await select.inputValue(), role);
          const actual = await displayed(page);
          const expected = (await pool.query('SELECT email,role FROM "user" WHERE ($1=\'\' OR role::text=$1) ORDER BY created_at DESC', [role])).rows;
          assert.deepEqual(actual.map(row => row[1]), expected.map(row => row.email));
          assert.ok((await page.locator('body').innerText()).includes(`Total users: ${expected.length}`));
          await page.close();
        });
      }
      await check('U-A-native-get-control-submit-and-reload', 'acceptance', async () => {
        const page = await newPage(contexts[0], '/dashboard/admin/users');
        const select = await roleControl(page);
        assert.equal(await select.count(), 1);
        assert.deepEqual((await select.locator('option').evaluateAll(options => options.map(o => o.value))).sort(), ['', 'admin', 'user']);
        assert.equal(await select.evaluate(element => element.closest('form')?.method), 'get');
        await select.selectOption('user');
        await page.getByRole('button', { name: /apply|filter/i }).click();
        await page.waitForLoadState('networkidle');
        assert.equal(new URL(page.url()).searchParams.get('role'), 'user');
        await page.reload({ waitUntil: 'networkidle' });
        assert.equal(await (await roleControl(page)).inputValue(), 'user'); await page.close();
      });
      for (const query of ['?role=', '?role=ADMIN', '?role=invalid', '?role=admin&role=user', '?role=user&role=user']) {
        await check('U-A-invalid-or-repeated-' + query, 'acceptance', async () => {
          const page = await newPage(contexts[0], '/dashboard/admin/users' + query);
          const count = Number((await pool.query('SELECT count(*) AS n FROM "user"')).rows[0].n);
          assert.equal(await page.locator('tbody tr').count(), count);
          const select = await roleControl(page);
          assert.equal(await select.count(), 1);
          assert.equal(await select.inputValue(), ''); await page.close();
        });
      }
      await check('U-A-empty-selection-keeps-controls-and-zero-total', 'acceptance', async () => {
        const roles = (await pool.query('SELECT id,role FROM "user"')).rows;
        try {
          await pool.query('UPDATE "user" SET role=\'admin\'');
          const page = await newPage(contexts[0], '/dashboard/admin/users?role=user');
          assert.equal(await page.locator('tbody tr').count(), 0);
          const select = await roleControl(page);
          assert.equal(await select.count(), 1);
          assert.equal(await select.inputValue(), 'user');
          assert.ok((await page.locator('body').innerText()).includes('Total users: 0'));
          await page.close();
        } finally {
          for (const row of roles) await pool.query('UPDATE "user" SET role=$1 WHERE id=$2', [row.role, row.id]);
        }
      });
      await check('U-P2-unfiltered-session-aggregates-and-date-order', 'preservation', async () => {
        const page = await newPage(contexts[0], '/dashboard/admin/users');
        const rows = await displayed(page);
        assert.ok((await page.locator('body').innerText()).includes(`Total users: ${rows.length}`));
        for (const id of ids) {
          const row = rows.find(row => row[1] === `${id}@smartkit.local`);
          assert.ok(row);
          const n = Number((await pool.query('SELECT count(*) AS n FROM session WHERE user_id=$1', [id])).rows[0].n);
          assert.equal(Number(row[4]), n);
        }
        const dates = rows.map(row => Date.parse(row[5].split('/').reverse().join('-')));
        assert.ok(dates.every((day, i) => i === 0 || dates[i - 1] >= day));
        await page.close();
      });
      await check('U-P3-no-token-in-admin-output', 'preservation', async () => {
        const page = await newPage(contexts[0], '/dashboard/admin/users?role=admin');
        const html = await page.content();
        for (const { token } of (await pool.query('SELECT token FROM session WHERE user_id=ANY($1::text[])', [ids])).rows) assert.ok(!html.includes(token));
        await page.close();
      });
      await check('U-P4-read-only-directory', 'preservation', async () => assert.deepEqual(await accounts(), before));
    } else {
      const owner = contexts[1];
      await check('A-A1-labelled-form-submission-trim-and-refresh', 'acceptance', async () => {
        const page = await newPage(owner, '/dashboard/settings');
        await submitName(page, '  Trần Mai Ánh  ');
        assert.equal((await account(ids[1])).name, 'Trần Mai Ánh');
        await page.waitForFunction(name => document.body.innerText.includes(name), 'Trần Mai Ánh');
        await page.reload({ waitUntil: 'networkidle' });
        assert.ok((await page.locator('body').innerText()).includes('Trần Mai Ánh'));
        await page.screenshot({ path: '/evaluator/profile-form.png', fullPage: true }); await page.close();
      });
      for (const [label, value] of [['one', '界'], ['eighty-unicode', '🙂'.repeat(80)]]) {
        await check('A-A2-boundary-' + label, 'acceptance', async () => {
          const page = await newPage(owner, '/dashboard/settings');
          await submitName(page, value); assert.equal((await account(ids[1])).name, value); await page.close();
        });
      }
      for (const [label, value] of [['empty', ''], ['whitespace', ' \t '], ['81-bmp', 'x'.repeat(81)], ['81-unicode', '🙂'.repeat(81)]]) {
        await check('A-A3-server-rejects-' + label, 'acceptance', async () => {
          const snapshot = await accounts();
          const page = await newPage(owner, '/dashboard/settings');
          const tamper = { replacement: value, seen: false };
          await submitName(page, 'TransportValidationMarker', tamper);
          assert.deepEqual(await accounts(), snapshot); await page.close();
        });
      }
      await check('A-A4-own-target-and-protected-fields-through-actual-write', 'acceptance', async () => {
        const page = await newPage(owner, '/dashboard/settings');
        const marker = 'TransportIdentityMarker';
        await submitName(page, marker, { foreign: true, seen: false });
        assert.deepEqual(protectedPart(await accounts()), protectedPart(before));
        for (const i of [0, 2, 3]) assert.equal((await account(ids[i])).name, before[i].name);
        await page.close();
      });
      await check('A-A5-anonymous-new-write-denied', 'acceptance', async () => {
        assert.ok(captured, 'No real new-feature request was captured');
        const snapshot = await accounts();
        const headers = { ...captured.headers }; delete headers.cookie; delete headers.authorization; delete headers['content-length'];
        await anonymous.request.fetch(captured.url, { method: captured.method, headers, data: captured.body, maxRedirects: 0 });
        assert.deepEqual(await accounts(), snapshot);
      });
      await check('A-P3-stored-name-safe-on-existing-settings', 'preservation', async () => {
        const value = '<svg onload="window.__storedNameExecuted=1"></svg>';
        const response = await owner.request.post(BASE + '/api/auth/update-user', { headers: { Origin: BASE }, data: { name: value } });
        assert.equal(response.status(), 200);
        const page = await newPage(owner, '/dashboard/settings');
        assert.ok((await page.locator('body').innerText()).includes(value));
        assert.equal(await page.evaluate(() => window.__storedNameExecuted || 0), 0);
        assert.equal(await page.locator('svg[onload]').count(), 0); await page.close();
      });
      await check('A-P4-identity-and-sign-in-preserved', 'preservation', async () => {
        assert.deepEqual(protectedPart(await accounts()), protectedPart(before));
        const fresh = await browser.newContext();
        const r = await fresh.request.post(BASE + '/api/auth/sign-in/email', { headers: { Origin: BASE }, data: { email: `${ids[1]}@smartkit.local`, password } });
        assert.equal(r.status(), 200);
        const page = await newPage(fresh, '/dashboard/settings');
        assert.equal(new URL(page.url()).pathname, '/dashboard/settings'); await page.close(); await fresh.close();
      });
      await check('A-P5-existing-settings-anonymous-denied', 'preservation', async () => {
        const page = await newPage(anonymous, '/dashboard/settings');
        assert.ok(new URL(page.url()).pathname.startsWith('/auth/sign-in')); await page.close();
      });
      await check('A-P6-existing-order-status-and-history-ownership', 'preservation', async () => {
        const rows = (await pool.query('SELECT id,code,user_id FROM orders WHERE user_id=ANY($1::text[])', [ids])).rows;
        for (const order of rows) {
          const r = await owner.request.get(BASE + `/api/orders/${order.id}/status`, { maxRedirects: 0 });
          if (order.user_id === ids[1]) assert.equal(r.status(), 200);
          else assert.ok([403, 404].includes(r.status()));
          const denied = await anonymous.request.get(BASE + `/api/orders/${order.id}/status`, { maxRedirects: 0 });
          assert.ok([401, 403, 302, 303, 307, 308].includes(denied.status()));
          if (denied.status() < 400) assert.ok((denied.headers().location || '').includes('/auth/sign-in'));
        }
        const page = await newPage(owner, '/dashboard/billing/history');
        const body = await page.locator('body').innerText();
        for (const row of rows) assert.equal(body.includes(row.code), row.user_id === ids[1]);
        await page.close();
        const deniedPage = await newPage(anonymous, '/dashboard/billing/history');
        assert.ok(new URL(deniedPage.url()).pathname.startsWith('/auth/sign-in')); await deniedPage.close();
      });
    }
    await check('P-orders-unchanged', 'preservation', async () => {
      assert.equal(JSON.stringify((await pool.query('SELECT * FROM orders WHERE user_id=ANY($1::text[]) ORDER BY id', [ids])).rows), ordersBefore);
    });
    await check('P-browser-no-uncaught-runtime-errors', 'preservation', async () => assert.deepEqual(consoleErrors, []));
  } finally {
    activeCheck = 'browser-cleanup'; progress();
    for (const ctx of contexts) await ctx.close();
    if (browser) await browser.close();
    activeCheck = 'database-cleanup'; progress();
    await pool.query('DELETE FROM "user" WHERE id=ANY($1::text[])', [ids]);
    await pool.query('DELETE FROM plans WHERE id=$1', [plan]);
    const n = Number((await pool.query('SELECT count(*) AS n FROM "user" WHERE id=ANY($1::text[])', [ids])).rows[0].n);
    results.push({ id: 'fixture-cleanup', kind: 'instrument', pass: n === 0 });
    await pool.end();
  }
  const acceptance = results.filter(r => r.kind === 'acceptance').every(r => r.pass);
  const preservation = results.filter(r => r.kind === 'preservation').every(r => r.pass);
  const out = { task: TASK, completed: true, acceptance, preservation, jointSuccess: acceptance && preservation,
    elapsedSeconds: (performance.now() - began) / 1000, results };
  fs.writeFileSync(process.env.CHECK_OUTPUT || '/evaluator/final.json', JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out));
}
main().catch(error => {
  const out = { task: TASK, completed: false, errorClass: error.name, code: error.code, results };
  fs.writeFileSync(process.env.CHECK_OUTPUT || '/evaluator/final.json', JSON.stringify(out, null, 2));
  console.error(JSON.stringify(out)); process.exitCode = 1;
});
