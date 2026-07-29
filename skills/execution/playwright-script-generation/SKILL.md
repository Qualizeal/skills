---
name: playwright-script-generation
description: Turning designed test cases into Playwright code — the translation contract, spec templates, data-driven and API-hybrid patterns, codegen workflow, and the review checklist generated scripts must pass. Use when automating manual test cases, scaffolding new specs, or reviewing generated test code.
---

# Script generation

Generating a test is a translation, not an invention. The input is a designed test case; the output is code that verifies exactly that case and nothing else. Scripts that quietly expand scope are how suites become slow and ambiguous.

## The translation contract

| Test case field | Becomes |
|---|---|
| ID + title | `test('...')` name, with the case ID in the title or an annotation |
| Preconditions | Fixture setup, via API |
| Steps | Actions on page objects |
| Expected result | Exactly one `expect` block |
| Data | A reference to a synthetic data profile |
| Priority | A tag: `@p0`, `@smoke` |

Rules that follow from this:

1. **One case, one test.** Never merge two cases because they share setup — share a fixture instead.
2. **Never invent an assertion.** If the case does not specify it, it is not verified here. Note the gap and route it back to test design.
3. **Never automate an ambiguous case.** "Verify the page loads correctly" cannot be translated. Send it back rather than guessing what "correctly" means, because your guess becomes the de facto spec.
4. **Preconditions go through the API.** Driving the UI to reach a starting state makes setup failures look like behaviour failures.

## Spec template

```ts
import { test, expect } from '../../fixtures';

test.describe('Checkout — promo codes', () => {
  test(
    'TC-412 rejects an expired promo code @p0',
    { annotation: [{ type: 'case', description: 'TC-412' }] },
    async ({ checkoutPage, order }) => {
      // Precondition: order created via API by the `order` fixture
      await checkoutPage.goto(order.id);

      // Action
      await checkoutPage.applyPromo('EXPIRED2024');

      // Expected: one specific, observable outcome
      await expect(page.getByRole('alert')).toHaveText(
        'This promo code expired on 31 December 2024',
      );
      await expect(checkoutPage.orderTotal).toHaveText('£128.40');
    },
  );
});
```

Structure every test as **Arrange → Act → Assert**, in that order, with no interleaving. A test that asserts, acts, asserts again is usually two tests.

## Data-driven cases

Boundary sets translate to a loop over a table — but generate a *separate test per row* so failures identify the row.

```ts
const promoCases = [
  { code: 'SAVE10',    discount: '£12.84', label: 'ten percent off' },
  { code: 'FLAT5',     discount: '£5.00',  label: 'flat five pounds' },
  { code: 'MINSPEND',  discount: '£0.00',  label: 'below minimum spend' },
];

for (const { code, discount, label } of promoCases) {
  test(`applies ${label} for ${code}`, async ({ checkoutPage, order }) => {
    await checkoutPage.goto(order.id);
    await checkoutPage.applyPromo(code);
    await expect(checkoutPage.discountLine).toHaveText(discount);
  });
}
```

Never loop *inside* one test with assertions per iteration. The first failure stops the loop and you lose the results of every remaining row.

## API + UI hybrid

The default shape for anything beyond a pure UI interaction:

```ts
test('TC-518 order appears in history after purchase @p1', async ({ api, page }) => {
  // Arrange via API — fast and unambiguous
  const order = await api.createOrder({ profile: 'single-item' });
  await api.completePayment(order.id);

  // Act via UI — the behaviour actually under test
  await page.goto('/account/orders');

  // Assert in both layers where it matters
  await expect(page.getByRole('row').filter({ hasText: order.reference })).toBeVisible();
  const persisted = await api.getOrder(order.id);
  expect(persisted.status).toBe('completed');
});
```

Assert through the UI for what the user sees, and through the API for what the system stored. A UI-only assertion cannot distinguish "displayed correctly" from "saved correctly".

## API test shape

Assert in three separate layers so a failure names the layer that broke:

```ts
test('POST /orders rejects a negative quantity', async ({ request }) => {
  const res = await request.post('/orders', { data: { sku: 'KB-01', quantity: -1 } });

  expect(res.status()).toBe(422);                       // transport
  const body = await res.json();
  expect(body).toMatchObject({ errors: expect.any(Array) });  // schema
  expect(body.errors[0].field).toBe('quantity');        // business
});
```

For GraphQL, also assert the `errors` array is absent — a 200 carrying errors is a failure, and a status-only assertion will pass straight over it.

## Codegen workflow

`npx playwright codegen <url>` is a starting point, never an output. Generated code is structurally correct and strategically poor: it records CSS selectors, absolute steps and no intent.

Always rewrite before committing:

1. Replace every recorded selector with the highest rung on the locator ladder that works
2. Delete recorded navigation that a fixture should perform via API
3. Replace recorded `waitFor` calls with web-first assertions
4. Extract repeated element access into a page object
5. Rename the test to state the behaviour and the expected outcome
6. Delete assertions codegen invented that the test case never asked for

Treat the recording as a map of the DOM, not as a draft of the test.

## Naming

```ts
test('rejects a payment when the card has expired')     // behaviour + outcome
test('shows an empty state when the order history is empty')

test('test payment 3')                                   // meaningless in a failure report
test('checkout works')                                   // works how?
```

The test name is what appears in a red pipeline at 6pm. Write it for that moment.

## Review checklist for generated scripts

- [ ] Traces to exactly one designed test case, referenced by ID
- [ ] Zero `waitForTimeout`
- [ ] Every locator justified against the priority ladder
- [ ] Setup via API, not UI
- [ ] Passes run alone, and passes run in parallel with the full suite
- [ ] Creates its own data and cleans up in a fixture, not in the test body
- [ ] One behaviour, one assertion block, Arrange-Act-Assert order
- [ ] No conditional logic (`if`/`try`) around assertions — branching means two tests
- [ ] Assertion messages specific enough to diagnose without opening a trace
- [ ] Tagged with priority; P0 tests belong in the smoke project
- [ ] No credentials, real customer data or hardcoded environment URLs

## When not to automate

Say so explicitly rather than producing a weak test:

- The case is ambiguous or the expected result is not observable
- The behaviour is genuinely exploratory or judgement-based (visual polish, copy tone)
- The setup cost exceeds the value and the case is P3
- The feature is changing next sprint — automate after it settles
- A unit or contract test would catch the same defect more cheaply
