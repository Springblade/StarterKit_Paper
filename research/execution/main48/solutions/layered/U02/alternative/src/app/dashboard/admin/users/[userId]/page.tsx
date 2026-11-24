import { eq,sql } from 'drizzle-orm';
import { notFound } from 'next/navigation';
import { db } from '@/database/db';
import { user,session } from '@/database/schema';
import { requireAdmin } from '@/lib/auth/auth';
export default async function AccountDetail({params}:{params:Promise<{userId:string}>}) {
 await requireAdmin();const {userId}=await params;
 const record=await db.query.user.findFirst({where:eq(user.id,userId),with:{sessions:{columns:{id:true}}}});if(!record)notFound();
 const count={n:record.sessions.length};
 if(!count)throw new Error('Missing session count');
 return <section><h2>Account detail</h2><dl>
 <dt>Name</dt><dd>{record.name}</dd><dt>Email</dt><dd>{record.email}</dd><dt>Role</dt><dd>{record.role}</dd>
 <dt>Verified</dt><dd>{record.emailVerified?'Yes':'No'}</dd><dt>Sessions</dt><dd>{count.n}</dd><dt>Created</dt><dd>{record.createdAt.toISOString()}</dd>
 </dl></section>;
}
