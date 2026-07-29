---
name: playwright-locator-strategy
description: "The six-rung locator priority ladder, filtering and chaining, lists and dynamic content, strict-mode violations, iframes and shadow DOM, test-id conventions and fragility scoring. Use when choosing, reviewing or repairing a selector."
---

# Playwright locator strategy

## The priority ladder

Use the first rung that works. Every step down increases coupling to things that are not behaviour.

| Rung | Locator | Couples to | Use when |
|---|---|---|---|
| 1 | `getByRole(role, { name })` | Accessible semantics | Always try first |
| 2 | `getByLabel` | Form semantics | Form fields |
| 3 | `getByPlaceholder`, `getByText`, `getByAltText`, `getByTitle` | Visible copy | Copy is stable, locale pinned |
| 4 | `getByTestId` | An explicit contract | Nothing above applies |
| 5 | CSS | Implementation | With a justification comment |
| 6 | XPath | DOM shape | Effectively never |

```ts
// Rung 1 — survives restyling, DOM restructuring, and framework migration
page.getByRole('button', { name: 'Place order' })

// Rung 4 — an explicit, greppable contract between app and test
page.getByTestId('order-total')

// Rung 5/6 — breaks on the next refactor
page.locator('div.sc-bdVaJa > button:nth-child(2)')
page.locator('//div[@class="cart"]/ul/li[3]/button')
```

`getByRole` has a second benefit that matters: an element you cannot address by role and accessible name is usually an element a screen reader user cannot address either. A locator failure at rung 1 is often an accessibility defect worth raising rather than routing around.

## Never use

- Generated class names (`.css-1x2y3z`, `.MuiBox-root-42`) — regenerate on every build
- Positional selectors (`nth-child`, `:first-of-type`) — break when a row is added
- Structural chains (`div > div > span`) — break on any wrapper change
- Auto-generated ids (`#react-aria-3`) — unstable across renders
- Untranslated visible text in an i18n app without pinning the locale

## Filtering and chaining

Scope narrowly rather than writing a more specific selector.

```ts
// Scope to a region, then locate within it
const summary = page.getByRole('region', { name: 'Order summary' });
await expect(summary.getByText('Free shipping')).toBeVisible();

// Filter a list by content
const row = page.getByRole('row').filter({ hasText: 'INV-1042' });
await row.getByRole('button', { name: 'Download' }).click();

// Filter by a descendant rather than by text
const card = page.getByTestId('product-card').filter({
  has: page.getByRole('heading', { name: 'Wireless keyboard' }),
});

// Exclude
const active = page.getByRole('listitem').filter({ hasNot: page.getByText('Archived') });
```

Chaining beats a clever single selector every time: each link is independently readable and independently fixable.

## Lists and dynamic content

Anchor on content, not position. `nth(2)` encodes an ordering assumption that the next sort-order change invalidates.

```ts
// Fragile — depends on ordering
await page.getByRole('row').nth(2).click();

// Stable — depends on identity
await page.getByRole('row').filter({ hasText: 'INV-1042' }).click();
```

Legitimate uses of `first()` / `nth()`: asserting a deliberate sort order ("the newest item appears first"), or iterating over a collection where identity genuinely does not matter.

## Strictness violations

Playwright throws when a locator resolves to more than one element. This is a feature — the error is telling you the test would otherwise have silently acted on an arbitrary element.

```
Error: strict mode violation: locator('button') resolved to 7 elements
```

Fix by narrowing, never by adding `.first()` to silence it. `.first()` on an accidentally ambiguous locator is a defect waiting to surface as a confusing failure.

```ts
// Wrong: silences the signal
page.getByRole('button').first()

// Right: says which button
page.getByRole('dialog', { name: 'Confirm' }).getByRole('button', { name: 'Delete' })
```

## Adding test ids to the application

When nothing semantic exists, change the application rather than reaching for CSS. This is a legitimate, normal code change — not test pollution.

```html
<span data-testid="order-total">£128.40</span>
```

Conventions:

- Kebab-case, describing the *thing*, not its styling: `order-total`, not `bold-right-text`
- Stable across refactors; treat it as a public contract and grep before changing one
- Put it on the element carrying the value, not on a wrapper
- Set `testIdAttribute` in the config once; do not hardcode `[data-testid=...]` in CSS selectors

## Iframes and shadow DOM

```ts
// Iframe: get a frame locator, then locate inside it
const payment = page.frameLocator('#payment-iframe');
await payment.getByLabel('Card number').fill('4111111111111111');

// Open shadow DOM: Playwright pierces it automatically — no special syntax
await page.getByRole('button', { name: 'Submit' }).click();
```

Closed shadow roots are not reachable. If the application uses them on elements you must test, that is an application change, not a test workaround.

## Assertions belong to locators

```ts
// Web-first: retries until true or times out
await expect(page.getByRole('alert')).toHaveText('Payment confirmed');
await expect(page.getByTestId('order-total')).toHaveText('£128.40');
await expect(page.getByRole('row')).toHaveCount(3);

// Not this: reads once, races the UI
const text = await page.getByRole('alert').textContent();
expect(text).toBe('Payment confirmed');
```

The second form is the most common source of "passes locally, fails in CI" in real suites.

## Review checklist

- [ ] Highest rung on the ladder that works?
- [ ] Any generated class, positional index or structural chain?
- [ ] Would this survive a CSS refactor? A component library upgrade? A copy change?
- [ ] Resolves to exactly one element, without `.first()` papering over ambiguity?
- [ ] Scoped to a region rather than relying on global uniqueness?
- [ ] Web-first assertion rather than a read-then-compare?
- [ ] New `data-testid` values follow the naming convention?

## Fragility scoring

Used by `script-maintainer` to rank the repair backlog:

| Signal | Score |
|---|---|
| `getByRole` with name | 0 |
| `getByLabel` / `getByText` | 1 |
| `getByTestId` | 2 |
| Stable CSS (semantic id) | 3 |
| Generated class or structural CSS | 5 |
| XPath | 8 |
| `+3` any hard wait in the same test | |
| `+4` order dependency | |
| `×` churn factor of the UI area (`git log` on the component) | |
