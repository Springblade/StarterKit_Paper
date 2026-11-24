import { z } from 'zod';

export const displayNameSchema = z.string().transform(value => value.trim()).refine(
  value => value.length >= 1 && value.length <= 80,
  'Display name must contain 1 to 80 Unicode code points after trimming.',
);
