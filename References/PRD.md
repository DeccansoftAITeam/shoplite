# ShopLite PRD

## Purpose and Scope
ShopLite is a minimal e-commerce training app for a 1-day workshop, built with React (Vite + TypeScript), FastAPI, and SQL Server using a monolithic modular architecture (router/service/repository per module).  
Scope is limited to: catalogue browsing (list + detail), cart, checkout (mock payment flow with status `PLACED`), order history, and search/filter.

## Catalog

**User story**  
As a shopper, I want to browse products and view product details so I can decide what to buy.

**Acceptance criteria**
1. **Given** products exist in the database, **when** I open the catalogue page, **then** I see a product list with at least name, price, and short description.
2. **Given** I am viewing the product list, **when** I select a product, **then** I can see a product detail view with full description, price, and stock availability indicator.
3. **Given** a product is out of stock, **when** I view its detail, **then** the UI clearly marks it as unavailable for adding to cart.

**Out-of-scope**
- Product reviews, ratings, recommendations, image galleries beyond a single image.
- Multi-currency, tax breakdowns, or promotional pricing logic.

## Cart

**User story**  
As a shopper, I want to add and manage items in my cart so I can prepare an order.

**Acceptance criteria**
1. **Given** I am on a product detail page, **when** I click “Add to cart” for an in-stock item, **then** the item appears in the cart with quantity `1`.
2. **Given** an item is already in my cart, **when** I increase or decrease quantity, **then** line totals and cart total update correctly.
3. **Given** an item is in my cart, **when** I remove it, **then** it no longer appears in the cart and totals recalculate.

**Out-of-scope**
- Persisting cart across devices or long-term sessions.
- Saved baskets, discount codes, shipping estimators.

## Checkout

**User story**  
As a shopper, I want to place my order from the cart so I can complete a purchase simulation.

**Acceptance criteria**
1. **Given** my cart has at least one item, **when** I submit checkout, **then** an order is created with status `PLACED`.
2. **Given** checkout is successful, **when** the order is created, **then** the cart is emptied.
3. **Given** my cart is empty, **when** I attempt checkout, **then** order placement is blocked with a clear validation message.

**Out-of-scope**
- Real payment gateways, payment failures, refunds, invoicing.
- Shipping integrations, delivery tracking, or fulfilment workflows.

## Orders

**User story**  
As a shopper, I want to view my past orders so I can confirm what I placed.

**Acceptance criteria**
1. **Given** I have placed orders, **when** I open order history, **then** I see a list ordered by newest first with order ID, date, total, and status.
2. **Given** I select an order from history, **when** the detail is shown, **then** I can see ordered items, quantities, and line totals.
3. **Given** I have no orders, **when** I open order history, **then** I see an empty-state message.

**Out-of-scope**
- Order cancellation, returns, exchanges, reordering.
- Email notifications or downloadable invoices.

## Search

**User story**  
As a shopper, I want to search and filter products so I can quickly find relevant items.

**Acceptance criteria**
1. **Given** I enter a keyword, **when** search is applied, **then** the catalogue list shows matching products by name (and optionally description).
2. **Given** filter options are available (e.g., category, price band, in-stock), **when** I apply filters, **then** results update to match all active filters.
3. **Given** no products match current search/filter criteria, **when** results render, **then** I see a clear “no results” state.

**Out-of-scope**
- Fuzzy matching, typo tolerance, synonyms, ranking algorithms.
- Advanced faceting, personalised search, or analytics-driven recommendations.

## Non-goals
- No authentication/authorisation.
- No real payments.
- No admin UI.
