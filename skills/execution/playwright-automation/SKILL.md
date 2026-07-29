---
name: playwright-automation
description: Playwright automation for web UI and REST/GraphQL APIs — the operating rules, plus routing into detailed references on framework architecture, locator strategy, script generation and the Playwright MCP/CLI browser loop. Use when writing, reviewing, scaffolding or debugging Playwright tests, choosing a selector, or driving a live browser to explore an application.
---

# Playwright automation

Automation that survives contact with a changing application. A suite that passes today and breaks next sprint on a CSS tweak is a liability, not an asset.

## Read this first, then load what you need

This skill carries the non-negotiables. The detail lives in four references — read the one the task calls for rather than all four:

| Reference | Read it when |
|---|---|
| `references/framework.md` | Setting up or changing the suite: `playwright.config.ts`, fixtures, page objects, auth and storage state, environments, parallelism, reporters |
| `references/locator-strategy.md` | Choosing or repairing a selector: the priority ladder, filtering and chaining, lists, strictness violations, iframes, test-id conventions |
| `references/script-generation.md` | Turning a designed test case into code: the translation contract, spec templates, data-driven and API-hybrid patterns, codegen rewriting, review checklist |
| `references/playwright-mcp.md` | Driving a live browser to explore, discover locators or reproduce a defect: the snapshot loop, MCP vs CLI token cost, configuration, safety guardrails |

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
