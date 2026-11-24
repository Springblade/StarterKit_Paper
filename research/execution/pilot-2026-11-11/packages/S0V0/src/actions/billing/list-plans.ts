'use server';

import { eq } from 'drizzle-orm';
import { db } from '@/database/db';
import { plans } from '@/database/schema/index';

export async function listPlans() {
  return db.query.plans.findMany({
    where: eq(plans.isActive, true),
    orderBy: (plans, { asc }) => [asc(plans.priceVnd)],
  });
}
