import { auth } from '@/features/auth/lib/auth';
export async function POST(request: Request) {
  if (request.headers.get('origin') !== new URL(request.url).origin) return Response.json({error:'Forbidden'}, {status:403});
  const data = await request.formData();
  const currentPassword=data.get('currentPassword'), newPassword=data.get('newPassword'), confirmation=data.get('confirmation');
  if (typeof currentPassword!=='string' || typeof newPassword!=='string' || newPassword!==confirmation || newPassword.length<8 || newPassword.length>128) return Response.json({error:'Invalid password input'}, {status:400});
  const session=await auth.api.getSession({headers:request.headers,query:{disableCookieCache:true}});
  if (!session) return Response.json({error:'Unauthorized'}, {status:401});
  try {
    const result=await auth.handler(new Request(new URL('/api/auth/change-password',request.url),{method:'POST',headers:{'Content-Type':'application/json',Origin:new URL(request.url).origin,Cookie:request.headers.get('cookie')??''},body:JSON.stringify({currentPassword,newPassword,revokeOtherSessions:false})}));
    if (!result.ok) return Response.json({error:'Password change rejected'}, {status:400});
    const response=Response.redirect(new URL('/dashboard/settings?password=saved',request.url),303);
    const headers=new Headers(response.headers);
    for (const cookie of result.headers.getSetCookie()) headers.append('set-cookie',cookie);
    return new Response(null,{status:303,headers});
  } catch { return Response.json({error:'Password change rejected'}, {status:400}); }
}
