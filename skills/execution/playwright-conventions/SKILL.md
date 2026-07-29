---
name: playwright-conventions
description: House standards for Playwright automation — locator priority, fixture patterns, web-first assertions, test independence, API-driven setup and project structure. Use when writing, reviewing or refactoring Playwright tests for web UI or REST/GraphQL APIs.
---

# Playwright conventions

## Locator priority

Use the first strategy that works. Every step down the list increases fragility.

1. `getByRole(role, { name })` — survives styling and structure changes, and tests accessibility as a side effect
2. `getByLabel` / `getByPlaceholder` / `getByText` — user-visible semantics
3. `getByTestId` — add `data-testid` to the application when nothing above applies
4. CSS — requires an inline justification comment
5. XPath — effectively forbidden; if you use it, explain why in the code

Never use: generated class names (`.css-1x2y3z`), `nth-child` positioning, structural chains (`div > div > span`), or text that is subject to i18n unless the locale is pinned.

## Web-first assertions, never sleeps

```
// Correct — retries until the condition holds or times out
await expect(page.getByRole('alert')).toHaveText('Payment confirmed');

// Wrong — passes locally, fails on a slow runner, hides a race
await page.waitForTimeout(2000);
```

`waitForTimeout` in a committed test is a defect. If a state genuinely needs waiting for, wait for the state, not the clock.

## Test independence

Every test must pass when run alone, in any order, and in parallel with others.

- Create the data the test needs; do not rely on seeded shared records that other tests mutate.
- Clean up in a fixture teardown, not at the end of the test body — the test body does not run after a failure.
- Never share mutable state between tests through module scope.
- If a test only passes in a suite run, it is order-dependent and broken.

## API-driven setup

Drive the UI only for the behaviour under test. Everything else — login, account creation, cart population, feature flag state — goes through the API in a fixture.

```
test.beforeEach(async ({ request }) => {
  // set up state via API: fast, reliable, and failures here are unambiguous
});
```

This makes setup failures distinguishable from behaviour failures, and cuts suite runtime substantially.

## Fixtures

Extend the base test with fixtures for authenticated context, seeded entities and API clients. Fixtures own creation *and* cleanup. Prefer fixtures over `beforeAll` for anything mutable.

## API and GraphQL testing

Assert in three separate layers so a failure identifies which one broke:

1. Transport — status code, headers
2. Schema — response shape against the contract file where one exists
3. Business — the actual values

For GraphQL, also assert the `errors` array is absent; a 200 with errors is a failure.

## Structure

```
tests/
  e2e/          # P0 journeys only
  api/
  fixtures/
  pages/        # page objects: locators and actions, never assertions
  data/         # references to synthetic data profiles
```

Page objects expose actions and locators. Assertions live in tests. A page object that asserts hides what a test is verifying.

## Naming

`test('rejects a payment when the card has expired', ...)` — behaviour and expected outcome. Not `test('test payment 3')`.

## Configuration

- Set `fullyParallel` and design tests to earn it.
- `retries: 1` maximum in CI, 0 locally, and report retried tests as flaky.
- Enable `trace: 'on-first-retry'` and `screenshot: 'only-on-failure'`.
- Pin the browser version in CI so a browser update cannot silently change results.
