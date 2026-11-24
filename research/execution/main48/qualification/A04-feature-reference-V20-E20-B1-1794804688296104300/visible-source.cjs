const {createRequire}=require('node:module');const req=createRequire('/workspace/package.json');req('dotenv').config({path:'/workspace/.env',quiet:true});
const {chromium}=require('/opt/behavior/node_modules/playwright');const {Pool}=req('pg');const assert=require('node:assert/strict');const {randomUUID}=require('node:crypto');
async function main(){
 assert.equal(new URL(process.env.DATABASE_URL).hostname,'pilot-db');const db=new Pool({connectionString:process.env.DATABASE_URL}),base='http://localhost:3107';const uid=randomUUID(),email=uid+'@local.invalid',old='Oldpass88',users=[],tokens=[],results=[];
 const {hashPassword}=await import(req.resolve('better-auth/crypto'));const hash=await hashPassword(old);const browser=await chromium.launch({headless:true,args:['--no-sandbox']});const c=await browser.newContext();
 async function check(id,fn){if(!id.startsWith('preservation-'))return;try{await fn();results.push({id,pass:true});}catch(e){results.push({id,pass:false,error:e.message});}console.log(JSON.stringify(results.at(-1)));}
 const api=(p,data)=>c.request.post(base+'/api/auth/'+p,{headers:{Origin:base},data});
 try{
  await db.query('INSERT INTO "user"(id,name,email,email_verified,role) VALUES($1,\'Fixture\',$2,true,\'user\')',[uid,email]);await db.query('INSERT INTO account(id,user_id,account_id,provider_id,password) VALUES($1,$2,$2,\'credential\',$3)',[randomUUID(),uid,hash]);
  await check('preservation-existing-short-password-login',async()=>{assert.equal((await api('sign-in/email',{email,password:old})).status(),200);});
  await check('preservation-reset-maximum128',async()=>{const token=randomUUID();tokens.push(token);await db.query('INSERT INTO verification(id,identifier,value,expires_at) VALUES($1,$2,$3,now()+interval\'1 hour\')',[randomUUID(),'reset-password:'+token,uid]);assert.equal((await api('reset-password',{token,newPassword:'p'.repeat(128)})).ok(),true);});
  await check('preservation-invalid-token-no-write-and-identity',async()=>{const before=(await db.query('SELECT password FROM account WHERE user_id=$1',[uid])).rows;assert.ok(!(await api('reset-password',{token:randomUUID(),newPassword:'validlongpassword'})).ok());assert.deepEqual((await db.query('SELECT password FROM account WHERE user_id=$1',[uid])).rows,before);const u=(await db.query('SELECT name,email,role,email_verified FROM "user" WHERE id=$1',[uid])).rows[0];assert.deepEqual(u,{name:'Fixture',email,role:'user',email_verified:true});});
 }finally{await browser.close();await db.query('DELETE FROM verification WHERE value=$1 OR identifier=ANY($2::text[])',[uid,tokens.map(t=>'reset-password:'+t)]);await db.query('DELETE FROM "user" WHERE id=$1 OR email=ANY($2::text[])',[uid,users]);await db.end();}
 const value={completed:true,pass:results.every(r=>r.pass),results};require('fs').writeFileSync(process.env.CHECK_OUTPUT||'/evaluator/visible.json',JSON.stringify(value));console.log(JSON.stringify(value));if(!value.pass)process.exitCode=1;
}
main().catch(e=>{console.error(e.name+': '+e.message);process.exitCode=1;});
