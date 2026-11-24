import 'server-only';
import { and, eq, sql } from 'drizzle-orm';
import { db } from '@/database/db';
import { orders, paymentTransactions } from '@/database/schema';

interface CompletionInput {
  sepayTransactionId: number;
  transferAmount: number;
  orderCode: string;
}

export type CompletionResult =
  | { status: 'completed'; orderId: string; planId: string; userId: string }
  | { status: 'ignored'; reason: 'order_not_found' | 'order_not_pending' | 'amount_mismatch' };

/**
 * Atomically complete an order matching `orderCode` from a SePay webhook.
 * Shared by the webhook handler and the cron polling fallback.
 *
 * Behavior matrix:
 * - `order_not_found`        → no order matches the code; caller should still have
 *                              recorded the payment transaction audit row.
 * - `order_not_pending`      → order exists but is already completed/expired/cancelled.
 * - `amount_mismatch`        → transfer amount differs from order amount.
 * - `completed`              → order was pending, amounts match, now flipped to completed.
 *
 * Note: idempotency on `payment_transactions.sepay_transaction_id` must already
 * have been checked by the caller. This helper assumes the caller has inserted
 * the audit row and decided to proceed with completion.
 */
export async function processOrderCompletion(input: CompletionInput): Promise<CompletionResult> {
  const { sepayTransactionId, transferAmount, orderCode } = input;

  return db.transaction(async (tx) => {
    await tx.select({id:orders.id}).from(orders).where(eq(orders.code,orderCode)).for('update');
    const clock = await tx.execute<{now:Date}>(sql`SELECT clock_timestamp() AS now`);
    const decisionTime = new Date(clock.rows[0]!.now);
    const updated = await tx.update(orders).set({
      status: sql`CASE WHEN ${orders.expiresAt} <= ${decisionTime} THEN 'expired'::order_status ELSE 'completed'::order_status END`,
      completedAt: sql`CASE WHEN ${orders.expiresAt} <= ${decisionTime} THEN NULL ELSE ${decisionTime}::timestamp END`,
    }).where(and(eq(orders.code,orderCode),eq(orders.status,'pending'),eq(orders.amountVnd,String(transferAmount)))).returning();
    const order = updated[0] ?? (await tx.select().from(orders).where(eq(orders.code,orderCode)).limit(1))[0];
    if (!order) return {status:'ignored',reason:'order_not_found'} as const;
    if (!updated.length && order.status==='pending') return {status:'ignored',reason:'amount_mismatch'} as const;
    await tx.update(paymentTransactions).set({orderId:order.id}).where(eq(paymentTransactions.sepayTransactionId,String(sepayTransactionId)));
    if (updated.length && order.status==='completed') return {status:'completed',orderId:order.id,planId:order.planId,userId:order.userId} as const;
    return {status:'ignored',reason:'order_not_pending'} as const;
  });
}
