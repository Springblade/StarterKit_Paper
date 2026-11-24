// Disposable local fixtures only. Output never contains cookies/passwords/tokens.
const {createRequire}=require('node:module');
const req=createRequire('/workspace/package.json');
req('dotenv').config({path:'/workspace/.env',quiet:true});
const {chromium}=require('/opt/behavior/node_modules/playwright');
const {Pool}=req('pg');const assert=require('node:assert/strict');const fs=require('node:fs');const {randomUUID}=require('node:crypto');
const base='http://localhost:3107',phase=process.env.PHASE||'baseline';
const dburl=new URL(process.env.DATABASE_URL);assert.equal(dburl.hostname,'pilot-db');assert.equal(dburl.pathname,'/smartkit_pilot');
const db=new Pool({connectionString:dburl.toString()});const results=[];const users=Array.from({length:4},()=>randomUUID());const plan=randomUUID(),order=randomUUID();
let browser;const contexts=[];
const save=()=>fs.writeFileSync('/evaluator/result.json',JSON.stringify({phase,modelCalls:0,completed:false,results},null,2));
async function check(id,fn){const start=Date.now();try{const observation=await fn();results.push({id,pass:true,seconds:(Date.now()-start)/1000,...(observation||{})});}catch(e){results.push({id,pass:false,errorClass:e.name,seconds:(Date.now()-start)/1000});}save();console.log(JSON.stringify(results.at(-1)));}
async function profile(id){return (await db.query('SELECT id,name,email,email_verified,role FROM "user" WHERE id=$1',[id])).rows[0];}
async function api(c,path,data){return c.request.post(base+path,{headers:{Origin:base},data});}
async function login(i,password){const c=await browser.newContext();contexts.push(c);const r=await api(c,'/api/auth/sign-in/email',{email:users[i]+'@smartkit.local',password});assert.equal(r.status(),200,'Fixture sign-in');return c;}
async function text(c,path){const page=await c.newPage();const r=await page.goto(base+path,{waitUntil:'networkidle',timeout:60000});const out={status:r.status(),url:page.url(),text:await page.locator('body').innerText(),page};return out;}
async function main(){
 const {hashPassword}=await import(req.resolve('better-auth/crypto'));const password='Local-only-'+randomUUID();const hash=await hashPassword(password);
 browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(let i=0;i<users.length;i++){
   await db.query('INSERT INTO "user"(id,name,email,email_verified,role,created_at) VALUES($1,$2,$3,true,$4,$5)',[users[i],'Feasibility '+i,users[i]+'@smartkit.local',i===0||i===3?'admin':'user',new Date(1700000000000+i*86400000)]);
   await db.query('INSERT INTO account(id,user_id,account_id,provider_id,password,created_at,updated_at) VALUES($1,$2,$2,\'credential\',$3,now(),now())',[randomUUID(),users[i],hash]);
  }
  await db.query('INSERT INTO plans(id,name,price_vnd) VALUES($1,\'Feasibility plan\',95000)',[plan]);
  await db.query('INSERT INTO orders(id,code,user_id,plan_id,amount_vnd,status,expires_at) VALUES($1,$2,$3,$4,95000,\'pending\',now()+interval\'1 hour\')',[order,'F-'+randomUUID(),users[1],plan]);
  const admin=await login(0,password),owner=await login(1,password),ordinary=await login(2,password),adminOther=await login(3,password);const anon=await browser.newContext();contexts.push(anon);
  await check('A01-A03-baseline-ui-gap',async()=>{const p=await text(owner,'/dashboard/settings');assert.equal(p.status,200);assert.equal(await p.page.locator('form').count(),0);assert.equal(await p.page.locator('a[href="/auth/reset-password"]').count(),1);await p.page.close();return {profileFormMissing:true,currentPasswordFormMissing:true,backendNotClaimedMissing:true};});
  await check('B03-baseline-resume-missing',async()=>{const before=(await db.query('SELECT id,code,amount_vnd,status,expires_at FROM orders WHERE id=$1',[order])).rows;const p=await text(owner,'/dashboard/billing?order='+order);assert.equal(p.status,200);assert.equal(await p.page.getByRole('heading',{name:'Payment Information',exact:true}).count(),0);assert.deepEqual((await db.query('SELECT id,code,amount_vnd,status,expires_at FROM orders WHERE id=$1',[order])).rows,before);await p.page.close();return {resumeQueryIgnored:true,orderUnchanged:true};});
  await check('B04-baseline-receipt-missing',async()=>{const p=await owner.request.get(base+'/api/orders/'+order+'/receipt');assert.equal(p.status(),404);return {receiptRouteStatus:p.status()};});
  await check('U02-U03-baseline-ui-gap',async()=>{const p=await text(admin,'/dashboard/admin/users');assert.equal(p.status,200);assert.equal(await p.page.locator('form').count(),0);assert.ok(p.text.includes(users[2]+'@smartkit.local'));await p.page.close();const r=await admin.request.get(base+'/dashboard/admin/users/'+users[2]);assert.equal(r.status(),404);return {roleControlsMissing:true,detailRouteStatus:r.status()};});
  await check('U03-existing-role-api-denies-ordinary-anonymous',async()=>{for(const c of[ordinary,anon]){const r=await api(c,'/api/auth/admin/set-role',{userId:users[2],role:'admin'});assert.ok([401,403].includes(r.status()));assert.equal((await profile(users[2])).role,'user');}});
  await check('U03-promotion-demotion-fresh-and-cached-session',async()=>{
   const original=await profile(users[2]);const r=await api(admin,'/api/auth/admin/set-role',{userId:users[2],role:'admin'});assert.equal(r.status(),200);assert.equal((await profile(users[2])).role,'admin');
   const promoted=await login(2,password);const page=await text(promoted,'/dashboard/admin/users');assert.equal(page.status,200);assert.ok(page.text.includes(users[0]+'@smartkit.local'));await page.page.close();
   const beforeCookies=await promoted.cookies();assert.ok(beforeCookies.some(c=>c.name.includes('session_data')));
   const d=await api(adminOther,'/api/auth/admin/set-role',{userId:users[2],role:'user'});assert.equal(d.status(),200);assert.equal((await profile(users[2])).role,'user');
   const cached=await browser.newContext();contexts.push(cached);await cached.addCookies(beforeCookies);
   const attempt=await api(cached,'/api/auth/admin/set-role',{userId:users[1],role:'admin'});assert.ok([401,403].includes(attempt.status()));assert.equal((await profile(users[1])).role,'user');
   const readContext=await browser.newContext();contexts.push(readContext);await readContext.addCookies(beforeCookies);const cr=await readContext.request.get(base+'/api/auth/get-session');assert.equal(cr.status(),200);const cachedUser=(await cr.json()).user;
   const fresh=await login(2,password);const denied=await text(fresh,'/dashboard/admin/users');assert.ok(!denied.text.includes(users[0]+'@smartkit.local'));await denied.page.close();
   assert.deepEqual(await profile(users[2]),original);
   return {oldCachedReadRole:cachedUser.role,currentDBRole:'user',oldCachedWriteStatus:attempt.status(),freshLoginAdminDataDenied:true};
  });
  await check('A03-existing-password-api-authentication-and-preservation',async()=>{
   const before=await profile(users[1]),beforeOrders=(await db.query('SELECT * FROM orders WHERE id=$1',[order])).rows;
   const newPass='Changed-'+randomUUID();const bad=await api(owner,'/api/auth/change-password',{currentPassword:'incorrect',newPassword:newPass,revokeOtherSessions:false});assert.ok([400,401,403].includes(bad.status()));
   assert.equal((await db.query('SELECT password FROM account WHERE user_id=$1',[users[1]])).rows[0].password,hash);
   const ok=await api(owner,'/api/auth/change-password',{currentPassword:password,newPassword:newPass,revokeOtherSessions:false});assert.equal(ok.status(),200);
   const tryOld=await api(anon,'/api/auth/sign-in/email',{email:users[1]+'@smartkit.local',password});assert.ok([400,401,403].includes(tryOld.status()));
   const fresh=await login(1,newPass);const s=await fresh.request.get(base+'/api/auth/get-session');assert.equal((await s.json()).user.id,users[1]);
   assert.deepEqual(await profile(users[1]),before);assert.deepEqual((await db.query('SELECT * FROM orders WHERE id=$1',[order])).rows,beforeOrders);
   await db.query('UPDATE account SET password=$1 WHERE user_id=$2',[hash,users[1]]);return {wrongCurrentRejected:true,oldPasswordRejected:true,newPasswordWorks:true,identityOrdersPreserved:true};
  });
  await check('baseline-role-api-self-demotion-scope',async()=>{const r=await api(adminOther,'/api/auth/admin/set-role',{userId:users[3],role:'user'});const after=await profile(users[3]);const result={status:r.status(),selfDemotionAllowed:after.role==='user',interpretation:'Existing API behavior only; new UI must enforce its own declared rule without repairing baseline'};await db.query('UPDATE "user" SET role=\'admin\' WHERE id=$1',[users[3]]);return result;});
 }finally{
  for(const c of contexts)await c.close();if(browser)await browser.close();
  await db.query('DELETE FROM orders WHERE user_id=ANY($1::text[])',[users]);await db.query('DELETE FROM plans WHERE id=$1',[plan]);for(const u of users)await db.query('DELETE FROM "user" WHERE id=$1',[u]);
  const remaining=Number((await db.query('SELECT count(*) AS n FROM "user" WHERE id=ANY($1::text[])',[users])).rows[0].n);assert.equal(remaining,0);await db.end();
 }
 const result={phase,modelCalls:0,completed:true,pass:results.every(r=>r.pass),baselineModified:false,browserAndRealDB:true,results};fs.writeFileSync('/evaluator/result.json',JSON.stringify(result,null,2));if(!result.pass)process.exitCode=1;
}
main().catch(e=>{save();console.error('Feasibility probe failed: '+e.name);process.exitCode=1;});
