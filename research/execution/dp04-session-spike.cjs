// Run only in a disposable pilot container; never print cookies or session tokens.
const { createRequire } = require('node:module');
const appRequire = createRequire('/workspace/package.json');
appRequire('dotenv').config({ path: '/workspace/.env', quiet: true });
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { Pool } = appRequire('pg');
const fs = require('node:fs');
const base = 'http://localhost:3107';
const database = new URL(process.env.DATABASE_URL);
assert.equal(database.hostname, 'pilot-db');
assert.equal(database.pathname, '/smartkit_pilot');
const pool = new Pool({ connectionString: database.toString() });
const users = [randomUUID(), randomUUID()];
const observations = [];
function cookieHeader(jar) {
  return [...jar].map(([name, value]) => `${name}=${value}`).join('; ');
}
async function request(path, jar, body) {
  const response = await fetch(base + path, {
    method: body === undefined ? 'GET' : 'POST',
    headers: { Cookie: cookieHeader(jar), Origin: base, 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
    redirect: 'manual', signal: AbortSignal.timeout(45000),
  });
  for (const raw of response.headers.getSetCookie()) {
    const pair = raw.split(';')[0];
    const cut = pair.indexOf('=');
    const name = pair.slice(0, cut), value = pair.slice(cut + 1);
    if (value) jar.set(name, value); else jar.delete(name);
  }
  return response;
}
async function session(jar, query = '') {
  const response = await request('/api/auth/get-session' + query, jar);
  assert.equal(response.status, 200);
  return response.json();
}
async function protectedPage(jar) {
  const response = await request('/dashboard/settings', jar);
  const html = await response.text();
  return {
    status: response.status,
    redirectedToSignIn: (response.headers.get('location') || '').includes('/auth/sign-in'),
    renderedProfile: response.status === 200 && html.includes('Manage your account settings'),
  };
}
async function main() {
  const { hashPassword } = await import(appRequire.resolve('better-auth/crypto'));
  const password = 'Local-spike-' + randomUUID();
  const hash = await hashPassword(password);
  try {
    for (const [i, id] of users.entries()) {
      await pool.query('INSERT INTO "user" (id,name,email,email_verified,role) VALUES ($1,$2,$3,true,$4)',
        [id, `Session spike ${i}`, `${id}@smartkit.local`, 'user']);
      await pool.query('INSERT INTO account (id,user_id,account_id,provider_id,password,created_at,updated_at) VALUES ($1,$2,$2,$3,$4,now(),now())',
        [randomUUID(), id, 'credential', hash]);
    }
    const jars = [];
    for (const id of [users[0], users[0], users[1]]) {
      const jar = new Map();
      const response = await request('/api/auth/sign-in/email', jar, { email: `${id}@smartkit.local`, password });
      assert.equal(response.status, 200, 'Fixture login');
      const data = await session(jar);
      assert.equal(data.user.id, id);
      assert.ok([...jar.keys()].some(key => key.includes('session_data')), 'Cached cookie must actually exist');
      assert.equal((await protectedPage(jar)).renderedProfile, true);
      jars.push(jar);
    }
    const [current, other, foreign] = jars;
    const otherSession = await session(other);
    const foreignSession = await session(foreign);
    const otherToken = otherSession.session.token;
    const foreignToken = foreignSession.session.token;
    assert.notEqual((await session(current)).session.token, otherToken);
    const list = await request('/api/auth/list-sessions', current);
    assert.equal(list.status, 200);
    const listed = await list.json();
    assert.ok(Array.isArray(listed));
    assert.ok(listed.some(item => item.token === otherToken));
    assert.ok(listed.every(item => item.userId === users[0]));
    observations.push({ check: 'list-sessions-owner-isolation', pass: true });

    const foreignRevoke = await request('/api/auth/revoke-session', current, { token: foreignToken });
    assert.ok([200, 400, 401, 403].includes(foreignRevoke.status));
    assert.equal(Number((await pool.query('SELECT count(*) AS n FROM session WHERE token=$1', [foreignToken])).rows[0].n), 1);
    observations.push({ check: 'foreign-session-not-revoked', pass: true, responseStatus: foreignRevoke.status });

    const capturedOther = new Map(other);
    const revoke = await request('/api/auth/revoke-session', current, { token: otherToken });
    assert.equal(revoke.status, 200);
    assert.equal(Number((await pool.query('SELECT count(*) AS n FROM session WHERE token=$1', [otherToken])).rows[0].n), 0);
    observations.push({ check: 'revoked-session-deleted-from-real-database', pass: true });

    // First protected request after revocation retains the victim's full cached cookie jar.
    const next = await protectedPage(new Map(capturedOther));
    const cached = await session(new Map(capturedOther));
    const authoritative = await session(new Map(capturedOther), '?disableCookieCache=true');
    const tokenOnly = new Map([...capturedOther].filter(([key]) => !key.includes('session_data')));
    const uncached = await protectedPage(tokenOnly);
    assert.equal(authoritative, null, 'DB-authoritative session lookup must reject revoked token');
    assert.equal(uncached.renderedProfile, false);
    assert.equal(uncached.redirectedToSignIn, true);
    assert.equal((await protectedPage(current)).renderedProfile, true);
    assert.equal((await protectedPage(foreign)).renderedProfile, true);
    observations.push({ check: 'current-and-foreign-protected-access-preserved', pass: true });
    observations.push({
      check: 'immediate-next-protected-request-with-real-cached-cookies',
      requirementPass: !next.renderedProfile && next.redirectedToSignIn,
      nextProtectedRequest: next,
      cachedLookupStillAuthenticated: cached?.user?.id === users[0],
      authoritativeLookupRejects: authoritative === null,
      withoutSessionDataCookie: uncached,
    });
    const result = {
      completed: true, runtime: 'real HTTP authentication and PostgreSQL; no auth/cache mocks',
      baselineModified: false, browserInteractionTested: false,
      immediateInvalidationPass: !next.renderedProfile && next.redirectedToSignIn,
      observations,
    };
    fs.writeFileSync('/evaluator/result.json', JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
  } finally {
    for (const id of users) await pool.query('DELETE FROM "user" WHERE id=$1', [id]);
    const remaining = Number((await pool.query('SELECT count(*) AS n FROM "user" WHERE id=ANY($1::text[])', [users])).rows[0].n);
    assert.equal(remaining, 0);
    await pool.end();
  }
}
main().catch(error => {
  // Assertion output can contain tokens; retain only a safe error class.
  fs.writeFileSync('/evaluator/error.json', JSON.stringify({ completed: false, errorClass: error.name }));
  console.error('Session spike failed; safe error class:', error.name);
  process.exitCode = 1;
});
