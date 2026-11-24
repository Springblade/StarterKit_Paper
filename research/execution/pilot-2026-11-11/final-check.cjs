// Final development-pilot evaluator, copied only into a fresh scoring container.
// Independently authored sparse fixtures, not the agent-visible 4-states-per-user cases.
const { createRequire } = require('node:module');
const requireApp = createRequire('/workspace/package.json');
requireApp('dotenv').config({ path: '/workspace/.env', quiet: true });
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { Pool } = requireApp('pg');
const { JSDOM } = requireApp('jsdom');
const fs = require('node:fs');
const base = 'http://localhost:3107';
const url = new URL(process.env.DATABASE_URL);
assert.equal(url.pathname, '/smartkit_pilot');
assert.equal(url.hostname, 'pilot-db');
const pool = new Pool({ connectionString: url.toString() });
const results = [];
const people = [randomUUID(), randomUUID(), randomUUID()];
const planIds = [randomUUID(), randomUUID()];
const records = [];
const cookies = [];
async function check(name, kind, fn) {
  try { await fn(); results.push({ name, kind, pass: true }); }
  catch (error) { results.push({ name, kind, pass: false, error: String(error.message).slice(0,600) }); }
}
async function history(person, query = '') {
  const r = await fetch(base + '/dashboard/billing/history' + query, {
    headers: { Cookie: cookies[person] }, redirect: 'manual', signal: AbortSignal.timeout(20000),
  });
  assert.equal(r.status, 200);
  const html = await r.text();
  return { html, doc: new JSDOM(html, { url: base }).window.document };
}
function expected(person, status) {
  return records.filter(row => row.user === people[person] && (!status || row.status === status))
    .sort((a,b) => b.day - a.day).map(row => row.code);
}
function displayed(doc) {
  return [...doc.querySelectorAll('tbody tr')].map(row => row.querySelector('td')?.textContent.trim());
}
async function main() {
  const { hashPassword } = await import(requireApp.resolve('better-auth/crypto'));
  const password = 'Final-pilot-' + randomUUID();
  const hash = await hashPassword(password);
  for (let i=0; i<people.length; i++) {
    await pool.query('INSERT INTO "user" (id,name,email,email_verified,role) VALUES ($1,$2,$3,true,$4)',
      [people[i], `Scoring user ${i}`, `${people[i]}@smartkit.local`, 'user']);
    await pool.query('INSERT INTO account (id,user_id,account_id,provider_id,password,created_at,updated_at) VALUES ($1,$2,$2,$3,$4,now(),now())',
      [randomUUID(), people[i], 'credential', hash]);
  }
  for (let i=0; i<planIds.length; i++) {
    await pool.query('INSERT INTO plans (id,name,price_vnd) VALUES ($1,$2,$3)',
      [planIds[i], `Final plan ${i}`, i ? '112000' : '73000']);
  }
  for (const [person, status, plan, day] of [
    [0,'pending',0,7], [0,'pending',1,3], [0,'completed',0,5],
    [1,'expired',1,6], [1,'cancelled',0,2], [1,'completed',1,1],
  ]) {
    const row = { id:randomUUID(), code:'EVAL-'+randomUUID(), user:people[person], status, plan, day };
    records.push(row);
    await pool.query('INSERT INTO orders (id,code,user_id,plan_id,amount_vnd,status,expires_at,created_at,completed_at) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)',
      [row.id,row.code,row.user,planIds[plan],plan ? '112000':'73000',status,
       new Date(Date.now()+(status==='expired' ? -60000:3600000)), new Date(Date.UTC(2026,1,day)),
       status==='completed' ? new Date(Date.UTC(2026,1,day,1)):null]);
  }
  for (const person of people) {
    const r = await fetch(base+'/api/auth/sign-in/email', {
      method:'POST',headers:{'Content-Type':'application/json',Origin:base},
      body:JSON.stringify({email:`${person}@smartkit.local`,password}),signal:AbortSignal.timeout(20000),
    });
    assert.equal(r.status,200,'Scoring fixture login failed');
    const cookie=r.headers.getSetCookie().map(value=>value.split(';')[0]).join('; ');
    assert.ok(cookie.includes('session_token'));
    cookies.push(cookie);
  }
  const snapshot = async () => JSON.stringify((await pool.query('SELECT * FROM orders ORDER BY id')).rows);
  const before = await snapshot();
  for (const person of [0,1]) {
    await check(`unfiltered-own-order-and-information-${person}`,'preservation',async()=>{
      const {html,doc}=await history(person);
      assert.deepEqual(displayed(doc),expected(person));
      for (const row of records.filter(row=>row.user!==people[person])) assert.ok(!html.includes(row.code));
      for (const row of doc.querySelectorAll('tbody tr')) {
        assert.ok(row.textContent.includes('Final plan'));
        assert.ok(row.textContent.includes('VND'));
      }
    });
    for (const status of ['pending','completed','cancelled','expired']) {
      await check(`subset-${person}-${status}`,'acceptance',async()=>{
        const {doc}=await history(person,`?status=${status}`);
        assert.deepEqual(displayed(doc),expected(person,status));
        assert.equal(doc.querySelector('select[name="status"]')?.value,status);
      });
      await check(`no-foreign-data-${person}-${status}`,'preservation',async()=>{
        const {html}=await history(person,`?status=${status}`);
        for (const row of records.filter(row=>row.user!==people[person])) assert.ok(!html.includes(row.code));
      });
    }
  }
  await check('labelled-get-dropdown-submit-and-reset','acceptance',async()=>{
    const {doc}=await history(0,'?status=completed');
    const select=doc.querySelector('select[name="status"]');assert.ok(select);
    assert.ok(select.id && doc.querySelector(`label[for="${select.id}"]`)?.textContent.trim());
    assert.deepEqual([...select.options].map(option=>option.value).sort(),['','cancelled','completed','expired','pending']);
    assert.match(select.querySelector('option[value="completed"]').textContent,/paid/i);
    const form=select.closest('form');assert.ok(form);
    assert.equal((form.getAttribute('method')||'get').toLowerCase(),'get');
    assert.ok(form.querySelector('button[type="submit"],input[type="submit"]'));
    const action=new URL(form.getAttribute('action')||'/dashboard/billing/history',base);
    assert.equal(action.origin,base);assert.equal(action.pathname,'/dashboard/billing/history');
    action.searchParams.set('status','');
    assert.deepEqual(displayed((await history(0,action.search)).doc),expected(0));
  });
  for (const query of ['?status=','?status=PENDING','?status=__proto__','?status=completed&status=completed','?status=expired&status=pending']) {
    await check(`fallback-${query}`,'acceptance',async()=>{
      const {doc}=await history(0,query);
      assert.deepEqual(displayed(doc),expected(0));
      assert.equal(doc.querySelector('select[name="status"]')?.value,'');
    });
  }
  for (const person of [1,2]) {
    await check(`empty-filter-with-controls-${person}`,'acceptance',async()=>{
      const {doc}=await history(person,'?status=pending');
      assert.deepEqual(displayed(doc),[]);
      assert.equal(doc.querySelector('select[name="status"]')?.value,'pending');
      assert.match(doc.body.textContent,/no .*orders|no .*transactions/i);
      assert.ok([...doc.querySelectorAll('a')].some(link=> /all/i.test(link.textContent) &&
        new URL(link.href,base).pathname==='/dashboard/billing/history'));
    });
  }
  await check('status-endpoint-owner-and-foreign-order','preservation',async()=>{
    for (const row of records) {
      const r=await fetch(base+`/api/orders/${row.id}/status`,{headers:{Cookie:cookies[0]},redirect:'manual'});
      if(row.user===people[0]) {assert.equal(r.status,200);assert.equal((await r.json()).status,row.status);}
      else assert.ok([403,404].includes(r.status));
    }
  });
  await check('anonymous-filter-and-status-denied','preservation',async()=>{
    for(const path of ['/dashboard/billing/history?status=pending',`/api/orders/${records[0].id}/status`]) {
      const r=await fetch(base+path,{redirect:'manual'});
      assert.ok([302,303,307,308,401,403].includes(r.status));
      const text=await r.text();for(const row of records)assert.ok(!text.includes(row.code));
    }
  });
  await check('filter-requests-do-not-mutate-orders','preservation',async()=>assert.equal(await snapshot(),before));
}
main().catch(error=>{
  results.push({name:'evaluator-execution',kind:'infrastructure',pass:false,error:String(error.message).slice(0,600)});
}).finally(async()=>{
  try {await pool.query('DELETE FROM "user" WHERE id = ANY($1::text[])',[people]);
       await pool.query('DELETE FROM plans WHERE id = ANY($1::text[])',[planIds]);}
  finally {await pool.end();}
  const group=kind=>{const rows=results.filter(row=>row.kind===kind);return rows.length>0&&rows.every(row=>row.pass);};
  const output={results,acceptance:group('acceptance'),preservation:group('preservation'),
    evaluator_completed:!results.some(row=>row.kind==='infrastructure'),
    joint_success:group('acceptance')&&group('preservation')&&!results.some(row=>row.kind==='infrastructure')};
  fs.writeFileSync('/evaluator/result.json',JSON.stringify(output,null,2));
  console.log(JSON.stringify({checks:results.length,failed:results.filter(row=>!row.pass).map(row=>row.name),...Object.fromEntries(Object.entries(output).filter(([key])=>key!=='results'))}));
  process.exitCode=output.joint_success?0:1;
});
