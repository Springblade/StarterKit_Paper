// Common synthetic upstream/clock fixture. No hidden assertions or task answers.
const fs=require('node:fs');
const realFetch=globalThis.fetch,RealDate=Date;
const read=(file,fallback)=>{try{return JSON.parse(fs.readFileSync(file,'utf8'));}catch{return fallback;}};
const now=()=>read('/tmp/study-clock.json',null)?.now??RealDate.now();
function StudyDate(...args){if(!new.target)return new RealDate(now()).toString();return Reflect.construct(RealDate,args.length?args:[now()],new.target);}
Object.setPrototypeOf(StudyDate,RealDate);StudyDate.prototype=RealDate.prototype;
StudyDate.now=now;StudyDate.parse=RealDate.parse;StudyDate.UTC=RealDate.UTC;
globalThis.Date=StudyDate;
globalThis.fetch=async(input,options)=>{
 const url=new URL(typeof input==='string'?input:input instanceof URL?input.href:input.url);
 if(url.hostname==='api.sepay.vn'){
  if(url.pathname!=='/userapi/transactions/list')return new Response('{}',{status:404});
  fs.appendFileSync('/tmp/study-sepay-calls.jsonl',JSON.stringify({path:url.pathname,at:RealDate.now()})+'\n');
  const headers=new Headers(options?.headers??(input instanceof Request?input.headers:undefined));
  if(headers.get('authorization')!=='synthetic-study-only')return new Response('{}',{status:401});
  return Response.json({data:read('/tmp/study-sepay-fixture.json',[])});
 }
 return realFetch(input,options);
};
