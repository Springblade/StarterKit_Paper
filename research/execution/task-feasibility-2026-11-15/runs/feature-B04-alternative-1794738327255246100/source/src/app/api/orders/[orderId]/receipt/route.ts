import { and,eq } from 'drizzle-orm';
import { db } from '@/database/db';
import { orders,plans } from '@/database/schema';
import { auth } from '@/features/auth/lib/auth';
export async function GET(request:Request,{params}:{params:Promise<{orderId:string}>}) {
 const session=await auth.api.getSession({headers:request.headers});if(!session)return Response.json({error:'Unauthorized'},{status:401});
 const {orderId}=await params;
 const rows=await db.select({order:orders,plan:plans}).from(orders).innerJoin(plans,eq(orders.planId,plans.id)).where(and(eq(orders.id,orderId),eq(orders.userId,session.user.id),eq(orders.status,'completed'))).limit(1);
 const order=rows[0]?{...rows[0].order,plan:rows[0].plan}:undefined;
 if(!order || !order.completedAt)return Response.json({error:'Not found'},{status:404});
 return Response.json({code:order.code,plan:{id:order.planId,name:order.plan.name},amountVnd:order.amountVnd,completedAt:order.completedAt.toISOString()},{headers:{'Content-Disposition':'attachment; filename="receipt.json"','Cache-Control':'no-store'}});
}
