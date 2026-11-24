// Server-only exports - DO NOT import in Client Components
export { authConfig } from '@/services/auth/auth.config';
export {
  auth,
  getSession,
  isAdmin,
  requireAdmin,
  requireAuth,
} from '@/lib/auth/auth';
export { sendEmail } from '@/lib/auth/email';
export { ROLES } from '@/lib/auth/permissions';
