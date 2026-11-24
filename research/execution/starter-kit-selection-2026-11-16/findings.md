# Ch?n starter kit ??c l?p cho th? nghi?m SmartKit

Ng?y kh?o s?t: 16/11/2026. ??y l? screening c? m?c ti?u, ch?a ph?i t?ng ?i?u tra th? tr??ng hay qualification runtime. ?? ??c ngu?n ch?nh th?c, metadata GitHub REST v? source t?i snapshot c? th?; ch?a c?i dependencies, build hay ch?y candidate. Kh?ng s?a b? freeze `main48`, allocation, evaluator hay paper; kh?ng g?i model th?c nghi?m.

## K?t lu?n ?? xu?t

**?u ti?n kh?o s?t kh? thi `nextjs/saas-starter` tr??c**, n?u m?c ti?u l? b? sung m?t repository ??c l?p nh?ng gi? g?n stack SmartKit. **Open SaaS l? l?a ch?n m?nh ?? kh?o s?t kh? n?ng chuy?n giao sang framework kh?c**, n?u ch?p nh?n Wasp/code generation v? th?m c?ng chu?n h?a th? nghi?m. BoxyHQ l? d? ph?ng ph? h?p h?n khi tr?ng t?m chuy?n sang team/permissions/enterprise workflows. ??y l? th? t? kh?o s?t, ch?a ph?i quy?t ??nh nh?n v?o main study.

Kh?ng c? ?ng vi?n n?o trong kh?o s?t n?y ???c ch?ng minh v?a ph? bi?n, v?a ???c d?ng r?ng r?i trong production, v?a ch?y ???c ho?n to?n offline ngay l?p t?c. Kh?ng thay thi?u b?ng ch?ng b?ng l?i qu?ng b?.

## C?ch l?a ch?n v? gi?i h?n t?m ki?m

T?m c?c SaaS starter kits c? source c?ng khai v? lu?ng auth/account/dashboard; ?u ti?n Next.js/TypeScript ?? gi?m kho?ng c?ch framework v?i SmartKit, nh?ng gi? m?t ?ng vi?n kh?c stack ?? th?y r? ??nh ??i external validity. Ti?u ch? g?m: m?c ???c ch? ?; b?ng ch?ng t?i s? d?ng; gi?y ph?p/source c? th? ki?m tra; ho?t ??ng tr?n nh?nh ch?nh; lu?ng nghi?p v? hi?n h?u; kh? n?ng reset d? li?u v? c? l?p d?ch v? ngo?i; kh? n?ng t?o hai layout t??ng ???ng. Kh?ng ??nh gi? b?ng k?t qu? agent hay ch?n task theo ?i?u ki?n th?ng.

?? kh?o s?t s?u repository v? lo?i th?m m?t legacy template ?? archived. C?c truy v?n discovery g?m `open source SaaS starter kit Next.js GitHub authentication billing postgres saas-starter SaaS-Boilerplate` v? c?c truy v?n t?m downstream c?a `nextjs/saas-starter`; t?m th?m tr?c ti?p b?ng GitHub repository search. ??y kh?ng ph?i m?u ng?u nhi?n ho?c danh s?ch ??y ?? t?t c? kit ph? bi?n.

## D?u hi?u ch? ? v? maintenance

S? li?u GitHub REST ch?p ng?y 16/11/2026. Stars/forks l? t?n hi?u ch? ? v? sao ch?p, kh?ng ph?i active users, s? ?ng d?ng production hay th? ph?n. Kh?ng ?o t?c ?? t?ng stars g?n ??y n?n kh?ng g?i ??y l? b?ng x?p h?ng ??ang hot?. `updated_at` c? th? ??i v? t??ng t?c; `pushed_at` c? th? li?n quan nh?nh kh?c. Ng?y commit d??i ??y l? commit m?i nh?t tr?n default branch ?? ??c.

| Kit | Stars | Forks | License metadata | Commit default branch m?i nh?t | Nh?n x?t screening |
|---|---:|---:|---|---|---|
| [Open SaaS](https://github.com/wasp-lang/open-saas) | 16,325 | 1,978 | MIT | 11/11/2026 | Ch? ? l?n, ho?t ??ng source g?n ??y; Wasp kh?c framework |
| [Next.js SaaS Starter](https://github.com/nextjs/saas-starter) | 16,253 | 2,749 | MIT | 11/12/2025 | G?n stack SmartKit; maintenance nh?nh ch?nh kh? c? |
| [ixartz SaaS Boilerplate](https://github.com/ixartz/SaaS-Boilerplate) | 7,491 | 1,334 | MIT | 21/08/2026 | Clerk l? dependency v?n h?nh; Stripe kh?ng c? trong b?n free |
| [BoxyHQ](https://github.com/boxyhq/saas-starter-kit) | 4,974 | 1,240 | Apache-2.0 | 08/05/2026 | Workflows doanh nghi?p phong ph?; nhi?u d?ch v? v? maintenance c? |
| [Makerkit Lite](https://github.com/makerkit/nextjs-saas-starter-kit-lite) | 466 | 169 | MIT | 15/10/2026 | Supabase local v? b?ng ch?ng template reuse; Lite thi?u billing/team/admin |
| [OpenStarterKit](https://github.com/openstarterkit/nextjs-saas-starter-kit) | 26 | 12 | MIT | 12/11/2026 | Stack g?n, source/test phong ph? nh?ng ch?a ??p ?ng ti?u ch? ch? ? l?n |

Ngu?n metadata: [Next.js](https://api.github.com/repos/nextjs/saas-starter), [Open SaaS](https://api.github.com/repos/wasp-lang/open-saas), [ixartz](https://api.github.com/repos/ixartz/SaaS-Boilerplate), [BoxyHQ](https://api.github.com/repos/boxyhq/saas-starter-kit), [Makerkit Lite](https://api.github.com/repos/makerkit/nextjs-saas-starter-kit-lite), [OpenStarterKit](https://api.github.com/repos/openstarterkit/nextjs-saas-starter-kit). C?c s? v? ng?y ???c l?u trong `repository-metadata.json` c?ng tree/commit snapshots trong `sources/`; kh?ng suy ra m?c ?? an to?n ho?c ??y ?? ch?c n?ng t? license hay s? test files.

## 1. Next.js SaaS Starter: ?ng vi?n ?u ti?n cho ph?p so s?nh g?n stack

README ch?nh th?c m? t? Next.js, PostgreSQL, Drizzle, shadcn/ui; email/password v?i JWT cookie; user/team CRUD; Owner/Member; activity logs; Stripe checkout v? customer portal. ??y l? starter t?i gi?n v? t?i li?u h?c, kh?ng ph?i m?t h? th?ng qu?n tr? ??y ??. Source hi?n ghim Next.js `15.6.0-canary.59` v? React 19.1.0; kh?ng th? m? t? n? nh? m?t kit Next.js 16 ?ang ???c c?p nh?t th??ng xuy?n. [README](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/README.md), [package](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/package.json).

**V? sao ??ng ch?n:** nhi?u ch? ?, source do b?n ngo?i x?y d?ng, g?n Next.js/Postgres/Drizzle c?a SmartKit, nghi?p v? account/team r? v? code t??ng ??i g?n. M?t d?u hi?u xu?t x? b? sung l? template c? `vercel/nextjs-subscription-payments` ?? sunset v? ch?nh README d?n sang kit n?y; ?? l? s? gi?i thi?u t? upstream, kh?ng ph?i b?ng ch?ng s? ng??i d?ng production. [Legacy README](https://github.com/vercel/nextjs-subscription-payments#readme).

**?i?m ph?i gi?i quy?t tr??c main:** tree ??y ?? kh?ng th?y file `.test`/`.spec` ho?c c?u h?nh test ?? t?m; package kh?ng c? test script. Kh?ng c? ngh?a repository kh?ng t?ng ???c th?, nh?ng ch?a c? V0 behavioral suite s?n ?? k? th?a. Setup script c? t??ng t?c Stripe CLI; seed th?c s? g?i Stripe ?? t?o products/prices, n?n ch? thay DATABASE_URL ch?a ?? ?? reset ho?n to?n offline. C?n thi?t k? fixture t?i kho?n/team ??c l?p, x?c ??nh ph?n d?ch v? ngo?i gi? th?t ho?c adapter chung, v? ki?m tra baseline tr??c khi ??a v?o study. Kh?ng t? n?ng dependencies ?? gi?ng SmartKit m? kh?ng ghi nh?n bi?n th?. [Setup](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/lib/db/setup.ts), [seed](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/lib/db/seed.ts), [Stripe source](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/lib/payments/stripe.ts).

**H? task c? th? kh?o s?t, ch?a ph?i y?u c?u ?? ch?n:** validation ? account settings, quy?n membership/invitation, ??c/l?c activity history. Source c? c?c Server Actions li?n quan; ??y l? ?? xu?t nghi?n c?u, kh?ng ph?i production issues ???c x?c nh?n. Kh?ng gi? ??nh kit c? password-reset nh? SmartKit ho?c super-admin to?n h? th?ng; c?n ch?n t? h?nh vi th?c s? c?. Invitation email c?n TODO trong action ?? ??c, n?n kh?ng ch?n m?t task preservation ??i gi? lu?ng g?i email ho?n ch?nh ch?a t?n t?i. [Actions](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/app/(login)/actions.ts), [schema](https://github.com/nextjs/saas-starter/blob/6e33e58b1e553a41fe22e6b941a7229a002de361/lib/db/schema.ts).

## 2. Open SaaS: m?nh v? ch? ? v? s? ??c l?p framework

Open SaaS d?ng Wasp v?i React/Node/Prisma, auth, payments, dashboard, background jobs v? v? d? t?nh n?ng SaaS. Template app, blog/docs v? E2E n?m trong c?c th? m?c kh?c nhau; ??i t??ng c?n l?y l? app template, kh?ng ph?i to?n b? website t?i li?u. Default branch c? thay ??i g?n ng?y kh?o s?t. [Repository](https://github.com/wasp-lang/open-saas), [app specification](https://github.com/wasp-lang/open-saas/blob/main/template/app/main.wasp.ts), [local README](https://github.com/wasp-lang/open-saas/blob/main/template/app/README.md).

**??nh ??i khoa h?c:** th?m m?t framework kh?c gi?p th? kh? n?ng chuy?n giao r?ng h?n, nh?ng Wasp specification v? generated infrastructure khi?n can thi?p layout kh? ??ng nh?t v?i SmartKit. Ph?i ch?t ranh gi?i authored source v? generated output; kh?ng d?ng vi?c di chuy?n generated files nh? t??ng ???ng v?i di chuy?n module handwritten. Kh?ng suy ra ?kh?c repository? t? ??ng l? replication c?ng intervention. C?n c? l?p c?c d?ch v? email/payment/storage/AI c?a c?c workflow ???c ch?n, gi? build/compiler v? instructions nh?t qu?n gi?a cell.

**D?u hi?u s? d?ng:** b?i founder case study v? TurboReel do Wasp xu?t b?n ng?y 10/12/2024 m? t? s? d?ng Open SaaS. ??y l? l?i k? ???c nh? cung c?p ??ng, kh?ng ph?i ph?p ?o adoption ??c l?p; source SaaS Wasp t??ng ?ng ch?a ???c x?c minh t? GitHub organization li?n k?t. [Case study](https://docs.opensaas.sh/blog/2024-12-10-turboreel-os-ai-video-generator-built-with-open-saas/), [organization](https://github.com/TurboReel).

## 3. C?c l?a ch?n c?n l?i

**BoxyHQ:** Next.js Pages Router, NextAuth, Prisma/Postgres; c? team, members, invitations, roles, sessions, API keys v? integration enterprise. Source tree c? E2E cho nhi?u lu?ng n?y. C? source subscription/billing, nh?ng README c? ph?n m? t? ch?a ??ng nh?t v?i code; kh?ng coi presence c?a handler l? ch?ng minh to?n b? payment lifecycle ch?y ??ng. Scope enterprise c? th? qu? r?ng so v?i ng?n s?ch 900 gi?y v? task SmartKit. [README](https://github.com/boxyhq/saas-starter-kit/blob/abc9b686823cbfb4973c79bc36fea37a3244be6c/README.md), [schema](https://github.com/boxyhq/saas-starter-kit/blob/abc9b686823cbfb4973c79bc36fea37a3244be6c/prisma/schema.prisma), [E2E](https://github.com/boxyhq/saas-starter-kit/tree/main/tests/e2e). Nhi?u integration l? c?u h?nh c? th? ch?n, kh?ng k?t lu?n m?i integration ??u b?t bu?c cho m?i task.

**ixartz:** c? TypeScript/Next.js/Drizzle, test scripts v? PGlite local. Tuy nhi?n auth/organizations ph? thu?c Clerk hosted; b?ng free/paid ghi r? Better Auth self-host v? Stripe integration kh?ng thu?c b?n free. Kh?ng l?y qu?ng b? b?n Plus/Pro/Max l?m t?nh n?ng c?a repository MIT n?y. Ph? h?p h?n n?u ch?p nh?n bi?n thi?n d?ch v? auth; ?u ti?n th?p h?n cho reset auth ho?n to?n c?c b?. [Feature comparison](https://github.com/ixartz/SaaS-Boilerplate/blob/e3952a7ed5b0ef172ac4363c4644b8c334d1094b/README.md), [manifest](https://github.com/ixartz/SaaS-Boilerplate/blob/e3952a7ed5b0ef172ac4363c4644b8c334d1094b/package.json), [Playwright config](https://github.com/ixartz/SaaS-Boilerplate/blob/e3952a7ed5b0ef172ac4363c4644b8c334d1094b/playwright.config.ts).

**Makerkit Lite:** Next.js/Turborepo, Supabase auth/database, settings v? Playwright. Local Supabase c? th? h? tr? reset, nh?ng chi ph? t?i nguy?n ph?i ?o. Lite thi?u billing, teams v? super-admin ???c qu?ng b? cho paid kit; kh?ng d?ng con s? ?1000+ developers? c?a full product l?m s? ng??i d?ng Lite. URL c? `next-supabase-saas-kit-lite` redirect sang `nextjs-saas-starter-kit-lite`. [README](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/README.md), [manifest](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/package.json).

C? m?t b?ng ch?ng reuse m?nh h?n stars: metadata GitHub c?a [ZeitPal](https://github.com/cderinbogaz/zeitpal) ghi `template_repository` tr? t?i Makerkit Lite, ??ng th?i README c?ng b? m?t ?ng d?ng leave management v? ghi nh?n Makerkit. ?i?u n?y x?c nh?n m?t project downstream s? d?ng template, kh?ng ch?ng minh ?ang deploy hay c? kh?ch h?ng tr? ti?n. Kh?ng l?y c?c kh?ng ??nh ph?p l?/hi?u qu? kinh doanh trong README downstream l?m k?t qu? ?? x?c minh. [Metadata](https://api.github.com/repos/cderinbogaz/zeitpal).

**OpenStarterKit:** public code g?n Better Auth/Next.js/Postgres c?a SmartKit, c? Stripe v? nhi?u test files, nh?ng 26 stars/12 forks t?i snapshot hi?n t?i c?n y?u cho l? do ch?n ????c nhi?u ng??i ch? ??. Gi? nh? ?ng vi?n k? thu?t, kh?ng d?ng ?? ??p ?ng ti?u ch? adoption l?n. [README](https://github.com/openstarterkit/nextjs-saas-starter-kit/blob/0a6534eb9b510c9c91b956165ec18ccd248c0055/README.md).

**Legacy b? lo?i:** `vercel/nextjs-subscription-payments` archived v? README th?ng b?o ?? sunset. S? stars cao kh?ng ??o ng??c t?nh tr?ng ??. [Metadata](https://api.github.com/repos/vercel/nextjs-subscription-payments), [README](https://github.com/vercel/nextjs-subscription-payments#readme).

## M?c b?ng ch?ng v? s? d?ng th?c t?

- Stars/forks: ?? x?c minh b?ng API cho s?u kit; ch? ch?ng minh ch? ? v? fork.
- Public downstream: Makerkit Lite -> ZeitPal ???c x?c nh?n qua template metadata. Next.js Starter c? c?c repository ngo?i t? ch?c gi? h??ng d?n ngu?n v? m? t? project, nh? [WorkForceSyncSaas](https://github.com/AnwarAndargie/WorkForceSyncSaas), m?t course project theo README; b?ng ch?ng n?y y?u h?n metadata template lineage v? kh?ng ch?ng minh s?n ph?m production. [Saas_demo](https://github.com/noel319/Saas_demo) ph?n l?n gi? README starter n?n kh?ng t?nh nh? tri?n khai ??ng k? ?? x?c minh.
- Vendor/user account: TurboReel/Open SaaS c? case study; ?? ghi gi?i h?n b?n tr?n.
- Active production installations, doanh thu v? t?c ?? t?ng adoption: ch?a x?c minh. Kh?ng c? c? s? vi?t ?h?ng ngh?n c?ng ty ?ang d?ng? cho c?c public repositories n?y.

## H? qu? v?i thi?t k? nghi?n c?u

Vi?c th?m m?t kit ??c l?p c?i thi?n external validity so v?i ch? SmartKit, nh?ng hai kit v?n l? hai tr??ng h?p ???c ch?n c? ch? ??ch, kh?ng ph?i m?u ??i di?n to?n b? starter kits. N?n ??t c?u h?i v? title theo ph?m vi th?c s? ?o.

N?u gi? ng?n s?ch 48, m?t thi?t k? ?? th?o lu?n l? 2 kits ? 3 tasks/kit ? 4 conditions ? 2 repetitions. ??y ch? l? l?a ch?n ph?n b?; ch?a thay allocation ?? freeze v? ch?a ch?ng minh precision ??. Ph?i ch?n task h?p v?i workflow t?ng kit: kh?ng ?p m? SePay, pending-order expiry ho?c admin session model c?a SmartKit sang Stripe/team model kh?c r?i coi l? c?ng task. So s?nh intervention trong t?ng kit, sau ?? b?o kh?c bi?t v? heterogeneity gi?a kit; kh?ng coi th?nh c?ng c?a hai s?n ph?m nguy?n tr?ng l? hi?u ?ng t? ch?c m?.

?? tr?nh ch?n theo k?t qu?, ghi ti?u ch? v? th? t? feasibility tr??c khi g?i main agent: (1) pin snapshot/license/lockfile; (2) d?ng auth + workflow baseline v? reset l?p; (3) x?c ??nh V0 ?? h?nh vi, gi? m?i checks s?n c?; (4) d?ng hai layout t??ng ???ng, b?o to?n routes/logic; (5) thi?t k? task card, valid alternatives, preservation faults, hidden evaluator; (6) reliability/capture/reset/score; (7) kh?a protocol v? freeze m?i. Thi?t k? V0 gi?a repositories c?n minh b?ch: Next.js Starter kh?ng c? behavioral test scripts t??ng ???ng SmartKit s?n; t? b? sung ch?ng l? thay ??i setting ph?i c?ng b?, kh?ng ?m th?m g?i l? upstream suite.

Public repositories c? th? n?m trong d? li?u hu?n luy?n c?a model. Kh?ng th? b?o ??m ??c l?p v?i training exposure ch? b?ng snapshot m?i ho?c task m?i. ??y l? gi?i h?n c?n ghi tr??c, kh?ng ph?i l? do ph? nh?n m?i benchmark c?ng khai.

## B??c ti?p theo ???c ?? xu?t

Kh?o s?t runtime c? gi?i h?n cho **Next.js SaaS Starter**, v?i **Open SaaS** l? ph??ng ?n c? m?c ti?u cross-stack ho?c **BoxyHQ** n?u m?c ti?u l? enterprise/team behavior. Ch?a t? ??ng nh?n kit v?o main, ch?a mua template/d?ch v?, ch?a g?i model pilot, v? ch?a s?a freeze SmartKit c?. N?u ??i ??i t??ng ho?c allocation th? freeze hi?n t?i ch? c?n ?p d?ng thi?t k? m?t kit ?? ki?m ch?ng; nghi?n c?u m?i c?n h? s? admission ri?ng.

C?c file ngu?n/metadata ???c l?u k?m ?? ??i chi?u t?i th?i ?i?m kh?o s?t. Th?ng tin license ? ??y l? m? t? t? upstream v? GitHub metadata, kh?ng thay th? vi?c ki?m tra ?i?u ki?n ph?n ph?i artifact cu?i. Kh?ng c? nghi?n c?u adoption h? th?ng, runtime qualification ho?c security audit dependencies trong l??t screening n?y.
