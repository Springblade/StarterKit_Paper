'use server';

import { and, desc, eq } from 'drizzle-orm';
import { z } from 'zod';
import { db } from '@/database/db';
import { orders } from '@/database/schema';
import { getSession } from '@/features/auth/lib/auth';
import { BillingError } from '../errors';

const ListOrdersParamsSchema = z.object({
  status: z.enum(['pending', 'completed', 'expired', 'cancelled']).optional(),
  limit: z.number().int().positive().max(50).optional(),
});

export type ListOrdersParams = z.input<typeof ListOrdersParamsSchema>;

export async function listOrders(params?: z.infer<typeof ListOrdersParamsSchema>) {
  const session = await getSession();
  if (!session) throw new BillingError('UNAUTHORIZED');

  const parsed = ListOrdersParamsSchema.parse(params ?? {});

  const whereClause = and(
    eq(orders.userId, session.user.id),
    parsed.status ? eq(orders.status, parsed.status) : undefined,
  );

  const ordersList = await db.query.orders.findMany({
    where: whereClause,
    with: {
      plan: true,
      user: {
        columns: {
          id: true,
          email: true,
          name: true,
        },
      },
    },
    orderBy: [desc(orders.createdAt)],
    limit: parsed.limit,
  });

  return ordersList;
}
