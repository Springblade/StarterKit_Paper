import 'dotenv/config';
import assert from 'node:assert/strict';
import {randomUUID,createHmac} from 'node:crypto';
import {pool} from '@/database/db';
import {extractOrderCode,generatePaymentContent} from '@/services/billing/payment-content';
import {processSepayPayload} from '@/services/billing/process-sepay-payload';
import {cancelExpiredOrders} from '@/services/billing/cancel-expired-orders';

async function main(){
 assert.equal(new URL(process.env.DATABASE_URL!).hostname,'pilot-db');
 const task=process.env.TASK, results: {id:string,pass:boolean,error?:string}[]=[];
 async function check(id:string,fn:()=>Promise<void>|void){try{await fn();results.push({id,pass:true});}catch(e){results.push({id,pass:false,error:e instanceof Error?e.message:'unknown'});}console.log(JSON.stringify(results.at(-1)));}
 const uid=randomUUID(),pid=randomUUID(),ids:string[]=[];let serial=Math.floor(Math.random()*1e9);
 const sql=(q:string,p:unknown[]=[])=>pool.query(q,p);
 const make=async(expiry:number,status='pending')=>{const id=randomUUID();ids.push(id);const code='Ab'+id.replaceAll('-','').slice(0,10);await sql('INSERT INTO orders(id,code,user_id,plan_id,amount_vnd,status,expires_at) VALUES($1,$2,$3,$4,95000,$5,$6)',[id,code,uid,pid,status,new Date(expiry)]);return {id,code};};
 const payload=(code:string,amount=95000)=>({id:++serial,transferType:'in' as const,transferAmount:amount,content:'SK '+code});
 try{
  await sql('INSERT INTO "user"(id,name,email,email_verified,role) VALUES($1,$2,$3,true,\'user\')',[uid,'Replacement fixture',uid+'@local.invalid']);
  await sql('INSERT INTO plans(id,name,price_vnd) VALUES($1,\'Replacement fixture\',95000)',[pid]);
  if(task==='B05'){
   await check('preservation-standard-QR-mixed-case',()=>{for(const c of ['AbC12345','Ab_12-34','abc12345','12345','Z'.repeat(50)])assert.equal(extractOrderCode(generatePaymentContent(c)),c);});
   await check('acceptance-token-grammar',()=>{assert.equal(extractOrderCode('BANK SK AbC12345 REF'),'AbC12345');assert.equal(extractOrderCode('BANK\tSK\n12345 REF'),'12345');for(const c of ['SK 1234','SK '+ 'a'.repeat(51),'sk 12345','SK 12345 SK 67890','SK','SK abc!23'])assert.equal(extractOrderCode(c),null);});
   await check('preservation-standard-payment-through-webhook',async()=>{const o=await make(Date.now()+3600000);const p={...payload(o.code),gateway:'fixture',transactionDate:'',accountNumber:'',reference:'',description:''};const body=JSON.stringify(p),timestamp=String(Math.floor(Date.now()/1000));const signature=createHmac('sha256',process.env.SEPAY_WEBHOOK_SECRET!).update(timestamp+'.'+body).digest('hex');const res=await fetch('http://localhost:3107/api/sepay/webhook',{method:'POST',headers:{'content-type':'application/json','x-sepay-timestamp':timestamp,'x-sepay-signature':'sha256='+signature},body});assert.equal(res.status,200);assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,'completed');});
   await check('acceptance-embedded-payment-through-shared-processor',async()=>{const o=await make(Date.now()+3600000);const p=payload(o.code);p.content='BANK '+p.content+' REF';assert.equal((await processSepayPayload(p)).status,'completed');assert.equal((await processSepayPayload(p)).status,'already_processed');});
  }else{
   await check('preservation-live-completion-and-audit',async()=>{const o=await make(Date.now()+3600000),p=payload(o.code);assert.equal((await processSepayPayload(p)).status,'completed');assert.equal((await processSepayPayload(p)).status,'already_processed');const rows=(await sql('SELECT order_id FROM payment_transactions WHERE sepay_transaction_id=$1',[String(p.id)])).rows;assert.equal(rows.length,1);assert.equal(rows[0].order_id,o.id);});
   await check('acceptance-expired-before-cleanup-no-entitlement',async()=>{const o=await make(Date.now()-60000),p=payload(o.code);assert.equal((await processSepayPayload(p)).status,'ignored');const row=(await sql('SELECT status,completed_at FROM orders WHERE id=$1',[o.id])).rows[0];assert.equal(row.status,'expired');assert.equal(row.completed_at,null);assert.equal((await sql('SELECT order_id FROM payment_transactions WHERE sepay_transaction_id=$1',[String(p.id)])).rows[0].order_id,o.id);});
   await check('acceptance-exact-expiry-server-clock',async()=>{const tick=Date.now(),o=await make(tick),SavedDate=globalThis.Date;globalThis.Date=class extends SavedDate {constructor(value?:string|number|Date){super(value===undefined?tick:value instanceof SavedDate?value.getTime():value);}static now(){return tick;}} as DateConstructor;try{assert.equal((await processSepayPayload(payload(o.code))).status,'ignored');assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,'expired');}finally{globalThis.Date=SavedDate;}});
   await check('acceptance-expired-through-signed-webhook',async()=>{const o=await make(Date.now()-60000);const p={...payload(o.code),gateway:'fixture',transactionDate:'',accountNumber:'',reference:'',description:''};const body=JSON.stringify(p),timestamp=String(Math.floor(Date.now()/1000));const signature=createHmac('sha256',process.env.SEPAY_WEBHOOK_SECRET!).update(timestamp+'.'+body).digest('hex');const response=await fetch('http://localhost:3107/api/sepay/webhook',{method:'POST',headers:{'content-type':'application/json','x-sepay-timestamp':timestamp,'x-sepay-signature':'sha256='+signature},body});assert.equal(response.status,200);assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,'expired');});
   await check('preservation-mismatch-terminal-outbound',async()=>{const o=await make(Date.now()+3600000);assert.equal((await processSepayPayload(payload(o.code,1))).status,'ignored');assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,'pending');for(const status of ['expired','cancelled','completed']){await sql('UPDATE orders SET status=$1 WHERE id=$2',[status,o.id]);assert.equal((await processSepayPayload(payload(o.code))).status,'ignored');assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,status);}assert.equal((await processSepayPayload({...payload(o.code),transferType:'out'})).status,'ignored');});
   await check('acceptance-cleanup-race-and-distinct-payments',async()=>{for(let i=0;i<5;i++){const o=await make(Date.now()-60000);await Promise.all([processSepayPayload(payload(o.code)),processSepayPayload(payload(o.code)),cancelExpiredOrders()]);assert.equal((await sql('SELECT status FROM orders WHERE id=$1',[o.id])).rows[0].status,'expired');}});
   await check('preservation-concurrent-live-payments-one-completion',async()=>{const o=await make(Date.now()+3600000);const outcomes=await Promise.all([processSepayPayload(payload(o.code)),processSepayPayload(payload(o.code))]);assert.equal(outcomes.filter(x=>x.status==='completed').length,1);});
  }
 }finally{
  await sql('DELETE FROM payment_transactions WHERE order_id=ANY($1::text[]) OR sepay_transaction_id=ANY($2::text[])',[ids,Array.from({length:40},(_,i)=>String(serial-i))]);
  await sql('DELETE FROM orders WHERE user_id=$1',[uid]);await sql('DELETE FROM plans WHERE id=$1',[pid]);await sql('DELETE FROM "user" WHERE id=$1',[uid]);await pool.end();
 }
 if(results.some(x=>!x.pass))process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1;});
