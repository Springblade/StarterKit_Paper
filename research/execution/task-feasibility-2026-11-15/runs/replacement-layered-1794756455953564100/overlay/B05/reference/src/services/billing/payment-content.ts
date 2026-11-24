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
  const tokens = content.trim().split(/\s+/);
  const markers = tokens.flatMap((t,i) => t === OrderCodePrefix ? [i] : []);
  if (markers.length !== 1) return null;
  const code = tokens[markers[0]! + 1];
  return code && /^[A-Za-z0-9_-]{5,50}$/.test(code) ? code : null;
}

/**
 * Generate the unique description for a payment, embedded in QR content.
 */
export function generatePaymentContent(orderCode: string): string {
  return `${OrderCodePrefix} ${orderCode}`;
}
