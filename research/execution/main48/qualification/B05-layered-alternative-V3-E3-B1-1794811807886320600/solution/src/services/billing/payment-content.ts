import { OrderCodePrefix } from '@/types/billing';

/**
 * Pure helpers for parsing / generating SePay payment content.
 * No DB, no I/O — safe to import from client bundles.
 */

/**
 * Extract order code from SePay transaction content.
 * Format: "SK aBc12345" -> "aBc12345"
 */
export function extractOrderCode(content: string): string | null {
  if ([...content.matchAll(/(?:^|\s)SK(?=\s|$)/g)].length !== 1) return null;
  return /(?:^|\s)SK\s+([A-Za-z0-9_-]{5,50})(?=\s|$)/.exec(content)?.[1] ?? null;
}

/**
 * Generate the unique description for a payment, embedded in QR content.
 */
export function generatePaymentContent(orderCode: string): string {
  return `${OrderCodePrefix} ${orderCode}`;
}
