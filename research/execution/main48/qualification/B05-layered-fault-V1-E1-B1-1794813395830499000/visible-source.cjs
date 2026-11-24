// Public retained-behavior suite. Exercises only standard pre-task payments.
const {createRequire}=require('node:module'),req=createRequire('/workspace/package.json');req('dotenv').config({quiet:true});
const {Pool}=req('pg'),{randomUUID,createHmac}=require('node:crypto'),assert=require('node:assert/strict'),fs=require('node:fs');
const db=new Pool({connectionString:process.env.DATABASE_URL}),uid=randomUUID(),pid=randomUUID(),oid=randomUUID(),txid=Math.floor(Math.random()*1e9),code='Vis_'+randomUUID().slice(0,8),results=[];
async function main(){
 assert.equal(new URL(process.env.DATABASE_URL).hostname,'pilot-db');
 let browser,activeCheck='VP-standard-QR-payment-case-live-audit-retry';
 try{
  await db.query('INSERT INTO "user"(id,name,email,role,email_verified) VALUES($1,\'Visible payer\',$2,\'user\',true)',[uid,uid+'@local.invalid']);await db.query('INSERT INTO plans(id,name,price_vnd) VALUES($1,\'Visible plan\',42000)',[pid]);await db.query('INSERT INTO orders(id,code,user_id,plan_id,amount_vnd,status,expires_at) VALUES($1,$2,$3,$4,42000,\'pending\',now()+interval\'3 hours\')',[oid,code,uid,pid]);
  if(process.env.CHECK_TASK==='B05'){
   activeCheck='VP-existing-checkout-transfer-format';
   const {hashPassword}=await import(req.resolve('better-auth/crypto'));const pass='VisibleCheckoutPwd';await db.query('INSERT INTO account(id,user_id,account_id,provider_id,password) VALUES($1,$2,$2,\'credential\',$3)',[randomUUID(),uid,await hashPassword(pass)]);
   const {chromium}=require('/opt/behavior/node_modules/playwright');browser=await chromium.launch({headless:true,args:['--no-sandbox']});const c=await browser.newContext();assert.equal((await c.request.post('http://localhost:3107/api/auth/sign-in/email',{headers:{Origin:'http://localhost:3107'},data:{email:uid+'@local.invalid',password:pass}})).status(),200);const page=await c.newPage();page.setDefaultNavigationTimeout(60000);let covered=false;for(let i=0;i<8;i++){await page.goto('http://localhost:3107/dashboard/billing?plan='+pid,{waitUntil:'networkidle'});const created=(await db.query('SELECT code FROM orders WHERE user_id=$1 AND status=\'pending\'',[uid])).rows;assert.equal(created.length,1);assert.ok((await page.locator('body').innerText()).includes('SK '+created[0].code));if(/[A-Z]/.test(created[0].code)){covered=true;break;}}if(!covered){const e=new Error('No uppercase input code generated');e.name='FixtureGenerationError';throw e;}results.push({id:'VP-existing-checkout-transfer-format',pass:true});await db.query('UPDATE orders SET status=\'cancelled\' WHERE user_id=$1',[uid]);await db.query('UPDATE orders SET status=\'pending\' WHERE id=$1',[oid]);
  }
  activeCheck='VP-standard-QR-payment-case-live-audit-retry';
  const data={id:txid,gateway:'fixture',transactionDate:new Date().toISOString(),accountNumber:'fixture',content:'SK '+code,transferType:'in',transferAmount:42000,reference:'',description:''},body=JSON.stringify(data),timestamp=String(Math.floor(Date.now()/1000)),signature=createHmac('sha256',process.env.SEPAY_WEBHOOK_SECRET).update(timestamp+'.'+body).digest('hex');
  for(let i=0;i<2;i++){const response=await fetch('http://localhost:3107/api/sepay/webhook',{method:'POST',headers:{'content-type':'application/json','x-sepay-timestamp':timestamp,'x-sepay-signature':'sha256='+signature},body});assert.equal(response.status,200);}
  const order=(await db.query('SELECT status FROM orders WHERE id=$1',[oid])).rows[0];assert.equal(order.status,'completed');const audit=(await db.query('SELECT order_id FROM payment_transactions WHERE sepay_transaction_id=$1',[String(txid)])).rows;assert.equal(audit.length,1);assert.equal(audit[0].order_id,oid);results.push({id:'VP-standard-QR-payment-case-live-audit-retry',pass:true});
 }catch(e){if(e.name==='FixtureGenerationError')throw e;results.push({id:activeCheck,pass:false,errorClass:e.name});}
 finally{if(browser)await browser.close();await db.query('DELETE FROM payment_transactions WHERE sepay_transaction_id=$1',[String(txid)]);await db.query('DELETE FROM orders WHERE user_id=$1',[uid]);await db.query('DELETE FROM plans WHERE id=$1',[pid]);await db.query('DELETE FROM "user" WHERE id=$1',[uid]);await db.end();}
 const out={completed:true,pass:results.every(r=>r.pass),results};fs.writeFileSync(process.env.CHECK_OUTPUT||'/evaluator/visible.json',JSON.stringify(out));console.log(JSON.stringify(out));if(!out.pass)process.exitCode=1;
}
main().catch(e=>{console.error(e.name);process.exitCode=2;});
