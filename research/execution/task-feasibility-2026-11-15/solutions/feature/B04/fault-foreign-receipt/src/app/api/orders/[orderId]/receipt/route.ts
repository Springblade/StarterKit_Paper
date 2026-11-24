import { and,eq } from 'drizzle-orm';
import { db } from '@/database/db';
import { orders } from '@/database/schema';
import { auth } from '@/features/auth/lib/auth';
export async function GET(request:Request,{params}:{params:Promise<{orderId:string}>}) {
 const session=await auth.api.getSession({headers:request.headers});if(!session)return Response.json({error:'Unauthorized'},{status:401});
 const {orderId}=await params;
 const order=await db.query.orders.findFirst({where:and(eq(orders.id,orderId),eq(orders.status,'completed')),with:{plan:true}});
 if(!order || !order.completedAt)return Response.json({error:'Not found'},{status:404});
 return Response.json({code:order.code,plan:{id:order.planId,name:order.plan.name},amountVnd:order.amountVnd,completedAt:order.completedAt.toISOString()},{headers:{'Content-Disposition':'attachment; filename="receipt.json"','Cache-Control':'no-store'}});
}
