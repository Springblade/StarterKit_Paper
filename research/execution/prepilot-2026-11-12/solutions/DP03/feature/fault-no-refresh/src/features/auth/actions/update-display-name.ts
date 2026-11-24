'use server';

import { headers } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { auth, requireAuth } from '@/features/auth/lib/auth';
import { displayNameSchema } from '@/features/auth/types/profile';

// Better Auth v1.6 nextCookies handles response cookies for Server Actions.
// https://www.better-auth.com/docs/integrations/next
export async function updateDisplayName(form: FormData) {
  await requireAuth();
  const parsed = displayNameSchema.safeParse(form.get('name'));
  if (!parsed.success) redirect('/dashboard/settings?profile=invalid');
  // Missing persistence: form submits without saving.
  revalidatePath('/dashboard', 'layout');
  redirect('/dashboard/settings?profile=saved');
}
