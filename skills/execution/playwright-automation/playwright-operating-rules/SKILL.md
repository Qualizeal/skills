---
name: playwright-operating-rules
description: "The ten non-negotiable rules for Playwright tests and what to check before writing any of them. Use as the first read when writing, reviewing or scaffolding Playwright automation."
---

# Playwright operating rules

## The ten rules

These apply to every test, and a review should reject code that breaks any of them.

1. **Locate by role and accessible name first.** `getByRole`, then label/text, then `data-testid`. CSS needs a justification comment; XPath is effectively forbidden.
2. **No hard waits.** `waitForTimeout` in a committed test is a defect. Wait for state via web-first assertions, never for the clock.
3. **Web-first assertions only.** `await expect(locator).toHaveText(...)`, not read-then-compare. Read-then-compare races the UI and is the most common cause of "passes locally, fails in CI".
4. **Setup through the API.** Reach the state under test with API calls in fixtures; drive the UI only for the behaviour actually being tested.
5. **Every test is independent.** It creates its own data, cleans up in a fixture teardown, and passes alone, in any order, and in parallel.
6. **One behaviour per test.** Arrange, Act, Assert, in that order. A test that asserts, acts and asserts again is two tests.
7. **Never silence a strictness violation with `.first()`.** Ambiguity is the framework telling you the test would otherwise click an arbitrary element. Narrow the locator instead.
8. **Page objects hold locators and actions, never assertions.** The moment a page object asserts, the test stops saying what it verifies.
9. **Pin the browser version** in CI to match `@playwright/test`. Silent browser drift becomes "flaky tests" nobody can reproduce.
10. **Never automate an ambiguous test case.** "Verify the page loads correctly" cannot be translated. Send it back; your guess would become the de facto specification.

## Before writing anything

1. Read the existing suite and match its structure, naming, fixture pattern and assertion style. Consistency beats your preferred style.
2. Read `playwright.config.*` for projects, base URL, `testIdAttribute` and timeouts. Do not introduce settings that contradict it.
3. Confirm which test case you are automating, at which level. Reject E2E automation of anything an API or unit test could catch — see `test-case-design` for level assignment.

## Output

The test files, any new fixtures or page objects, a note on the locator strategy used per element and why, and the command to run the new tests in isolation.
