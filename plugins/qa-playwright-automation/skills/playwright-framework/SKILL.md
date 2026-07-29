---
name: playwright-framework
description: "Project structure, annotated playwright.config.ts, environment validation, storage-state authentication, fixture scoping, page objects, parallelism, network control and the anti-pattern table. Use when setting up or restructuring a Playwright suite."
---

# Playwright framework architecture

## Project structure

```
tests/
  e2e/                  # P0 user journeys only
    checkout.spec.ts
  api/                  # REST/GraphQL contract and behaviour
  components/           # component tests, if used
fixtures/
  index.ts              # the extended `test` object everything imports
  auth.fixture.ts
  data.fixture.ts
  network.fixture.ts
pages/                  # page objects: locators + actions, never assertions
  checkout.page.ts
support/
  api-client.ts         # typed HTTP client for setup and teardown
  env.ts                # validated environment config
  types.ts
data/
  profiles.ts           # references to synthetic data profiles
playwright.config.ts
```

Two rules keep this from rotting:

1. **Tests import from `fixtures/index.ts` and nowhere else.** One import line, one place to extend.
2. **Nothing in `pages/` asserts.** Page objects expose locators and actions. The moment a page object asserts, the test file stops telling you what is being verified.

## playwright.config.ts

```ts
import { defineConfig, devices } from '@playwright/test';
import { env } from './support/env';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,        // a stray .only silently skips the suite
  retries: process.env.CI ? 1 : 0,     // never retry locally: you would not see the flake
  workers: process.env.CI ? '50%' : undefined,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  reporter: process.env.CI
    ? [['blob'], ['github'], ['junit', { outputFile: 'results/junit.xml' }]]
    : [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: env.BASE_URL,
    testIdAttribute: 'data-testid',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: 'setup', testMatch: /global\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
    { name: 'api', testDir: './tests/api', use: { baseURL: env.API_URL } },
  ],
});
```

Notes on the choices that people get wrong:

- **`forbidOnly` in CI is not optional.** A committed `test.only` turns a 400-test suite into a 1-test suite that passes. Without this flag nobody notices for weeks.
- **`retries: 0` locally.** Retrying on a developer machine hides the flake at exactly the moment someone could have investigated it.
- **Global timeouts stay tight.** A 90-second test timeout does not fix flakiness; it converts a fast failure into a slow one and lengthens every CI run.
- **`blob` reporter in CI** so sharded runs can be merged into one HTML report (`npx playwright merge-reports`).

## Environment config

Validate at load, fail loudly. A suite that starts against an undefined `BASE_URL` produces confusing failures ten minutes later.

```ts
// support/env.ts
const required = ['BASE_URL', 'API_URL', 'TEST_USER_PASSWORD'] as const;

const missing = required.filter((k) => !process.env[k]);
if (missing.length) {
  throw new Error(`Missing required env vars: ${missing.join(', ')}`);
}

export const env = {
  BASE_URL: process.env.BASE_URL!,
  API_URL: process.env.API_URL!,
  TEST_USER_PASSWORD: process.env.TEST_USER_PASSWORD!,
  ENVIRONMENT: process.env.ENVIRONMENT ?? 'local',
} as const;
```

Never commit credentials. Never branch test *logic* on environment — branch configuration only. A test that behaves differently in staging is not testing staging.

## Authentication and storage state

Authenticate once in a setup project, reuse the state everywhere. Logging in through the UI in every test is the single largest avoidable cost in most suites.

```ts
// tests/global.setup.ts
import { test as setup, expect } from '@playwright/test';
import { env } from '../support/env';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('qa.user@example.com');
  await page.getByLabel('Password').fill(env.TEST_USER_PASSWORD);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  await page.context().storageState({ path: '.auth/user.json' });
});
```

For multi-role suites, produce one storage state per role (`.auth/admin.json`, `.auth/viewer.json`) and select it per project or per fixture. Add `.auth/` to `.gitignore` — it contains live session tokens.

## Fixtures

Fixtures own setup **and** teardown. Teardown in a test body does not run after a failure, so cleanup written there leaks state on exactly the runs where it matters.

```ts
// fixtures/index.ts
import { test as base } from '@playwright/test';
import { ApiClient } from '../support/api-client';
import { CheckoutPage } from '../pages/checkout.page';

type Fixtures = {
  api: ApiClient;
  order: { id: string };
  checkoutPage: CheckoutPage;
};

export const test = base.extend<Fixtures>({
  api: async ({ request }, use) => {
    await use(new ApiClient(request));
  },

  // Creates its own data, cleans it up, and never depends on another test.
  order: async ({ api }, use) => {
    const order = await api.createOrder({ profile: 'standard-cart' });
    await use(order);
    await api.deleteOrder(order.id);   // runs even when the test fails
  },

  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
});

export { expect } from '@playwright/test';
```

Fixture scoping:

- **`test` scope** (default) — anything mutable. Per-test data, per-test context.
- **`worker` scope** — expensive and read-only. A seeded reference dataset, a started container.
- Never share mutable state at worker scope. It reintroduces the test-order coupling that parallelism was meant to eliminate.

## Page objects

```ts
// pages/checkout.page.ts
import { Page, Locator } from '@playwright/test';

export class CheckoutPage {
  readonly promoCode: Locator;
  readonly placeOrder: Locator;
  readonly orderTotal: Locator;

  constructor(private page: Page) {
    this.promoCode = page.getByLabel('Promo code');
    this.placeOrder = page.getByRole('button', { name: 'Place order' });
    this.orderTotal = page.getByTestId('order-total');
  }

  async goto(orderId: string) {
    await this.page.goto(`/checkout/${orderId}`);
  }

  async applyPromo(code: string) {
    await this.promoCode.fill(code);
    await this.promoCode.press('Enter');
  }
}
```

- Locators are declared once as fields, not rebuilt inline in every method.
- Methods are user intentions (`applyPromo`), not mechanics (`typeIntoField`).
- No assertions, no `expect`, no waits beyond what actions do implicitly.
- No page object needs a `waitForLoad` method. If you find yourself writing one, the locators are wrong.

## Parallelism and isolation

`fullyParallel: true` is only safe if every test earns it:

- creates the data it needs, via API
- never mutates shared reference data
- never asserts on a global counter, a list length, or "the most recent" record
- never depends on execution order

Use `test.describe.configure({ mode: 'serial' })` sparingly and always with a comment explaining why. Serial mode means one failure skips the rest of the block, which hides information.

## Network control

```ts
// Stub only third parties you do not own. Stubbing your own API means
// testing your mocks rather than your integration.
await page.route('**/analytics.thirdparty.com/**', (route) => route.abort());

// Deterministic failure paths that are hard to trigger for real
await page.route('**/api/payment', (route) =>
  route.fulfill({ status: 503, body: JSON.stringify({ error: 'unavailable' }) }),
);
```

## Reporters and artefacts

CI publishes on failure, always: trace, screenshot, video, JUnit XML, and the blob report for merging. `trace: 'on-first-retry'` gives full timeline evidence on the run that failed without paying the tracing cost on every green run.

## Anti-patterns

| Anti-pattern | Why it hurts | Instead |
|---|---|---|
| `waitForTimeout` | Passes locally, fails on slow runners, hides races | Web-first assertions |
| Login through UI in every test | Dominates runtime; failures are ambiguous | Storage state + setup project |
| Assertions inside page objects | Tests no longer state what they verify | Assert in the test |
| Shared mutable fixture at worker scope | Reintroduces order coupling | Test-scoped fixtures |
| `if (env === 'staging')` in a test | You are no longer testing staging | Branch config, not logic |
| Raising a timeout to fix a flake | Converts a fast failure into a slow one | Fix the wait condition |
| One giant `helpers.ts` | Becomes a dumping ground nobody owns | Named fixtures and page objects |
