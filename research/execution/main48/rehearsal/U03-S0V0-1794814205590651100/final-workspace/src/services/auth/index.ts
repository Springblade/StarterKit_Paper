// Client-only exports - import only in Client Components
export { authClient, signIn, signOut, signUp, useSession } from '@/lib/auth/client';
export { ResetPasswordEmail, VerificationEmail, WelcomeEmail } from '@/emails/auth/index';
// Server-only exports - import only in Server Components / Server Actions
export {
  auth,
  authConfig,
  getSession,
  isAdmin,
  requireAdmin,
  requireAuth,
} from '@/lib/auth/index';

export { ROLES } from '@/lib/auth/permissions';

export type { AuthUser, LoginCredentials, RegisterCredentials } from '@/types/auth/index';
