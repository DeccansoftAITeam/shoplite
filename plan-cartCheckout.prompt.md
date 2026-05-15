**Plan: Cart And Checkout Lab**

Implement this as one DB-backed anonymous-cart slice: add new backend `cart` and `orders` modules, wire them into FastAPI and Alembic, then add frontend cart/checkout pages plus shared cart-count state. Scope stays tight to the requested endpoints and screens: `GET /api/cart`, `POST /api/cart/items`, `DELETE /api/cart/items/{product_id}`, and `POST /api/orders`; no tests, no `/orders` UI, and no separate backend `checkout` module for this lab.

**Backend**
1. Create `backend/app/modules/cart/models.py` with `Cart` and `CartItem` mapped to `carts` and `cart_items`, using DB persistence, a unique anonymous `cart_id`/session identifier, FK to `products.id`, quantity, `unit_price`, and UTC timestamps.
2. Create `backend/app/modules/cart/schemas.py` for add-item input, cart line output, and cart summary output, including totals as decimal-backed values.
3. Create `backend/app/modules/cart/repository.py` for all SQLAlchemy cart access: get-or-create cart by cookie ID, load cart with items, upsert/increment item quantity, remove item by `product_id`, and clear cart items after checkout.
4. Create `backend/app/modules/cart/service.py` for cart business rules only: resolve/create anonymous cart, validate product existence via the catalog service layer, optionally block out-of-stock adds, and compute totals.
5. Create `backend/app/modules/cart/router.py` for `GET /api/cart`, `POST /api/cart/items`, and `DELETE /api/cart/items/{product_id}`. This router should read/set the anonymous `cart_id` cookie and reuse the standard error payload from [core/errors.py](/d:/shoplite/backend/app/core/errors.py).
6. Create `backend/app/modules/orders/models.py` with `Order` and `OrderItem` mapped to `orders` and `order_items`, including `status='PLACED'`, `total_amount`, copied product snapshot fields, and `created_at`.
7. Create `backend/app/modules/orders/schemas.py` for the minimal checkout response contract: order id, status, total, and timestamp.
8. Create `backend/app/modules/orders/repository.py` for transactional order persistence: insert `orders`, insert `order_items` from the cart snapshot, and commit atomically.
9. Create `backend/app/modules/orders/service.py` to orchestrate checkout by calling the cart service, rejecting empty carts, creating the order with status `PLACED`, and clearing the cart only after successful order creation.
10. Create `backend/app/modules/orders/router.py` for `POST /api/orders`, reading the same `cart_id` cookie and returning standard validation/not-found errors as needed.
11. Add one Alembic revision under `backend/alembic/versions/` to create `carts`, `cart_items`, `orders`, and `order_items`, following the pattern in [ad76914b8a3b_initial_catalog_tables.py](/d:/shoplite/backend/alembic/versions/ad76914b8a3b_initial_catalog_tables.py).
12. Update [main.py](/d:/shoplite/backend/app/main.py) to register the new `cart` and `orders` routers.

**Frontend**
1. Create `frontend/src/api/cart.ts` with typed helpers for `fetchCart`, `addCartItem`, and `removeCartItem`, following the axios pattern in [catalog.ts](/d:/shoplite/frontend/src/api/catalog.ts).
2. Create `frontend/src/api/orders.ts` for `POST /api/orders`.
3. Create `frontend/src/context/CartContext.tsx` to centralize cart fetch/refresh and expose a shared `itemCount` plus mutation helpers to pages and the header.
4. Create `frontend/src/components/Header.tsx` with links to products and cart plus a live cart-count badge.
5. Update [App.tsx](/d:/shoplite/frontend/src/App.tsx) to wrap the app with the cart provider and header, and add routes for `/cart` and `/checkout`.
6. Update [ProductDetailPage.tsx](/d:/shoplite/frontend/src/pages/ProductDetailPage.tsx) to add an “Add to cart” action, disable it when stock is zero, and refresh shared cart state after success.
7. Create `frontend/src/pages/CartPage.tsx` to display cart lines, quantities, line totals, grand total, remove actions, empty-cart state, and a CTA to `/checkout`.
8. Create `frontend/src/pages/CheckoutPage.tsx` to show the current cart summary, block checkout when empty, call `POST /api/orders`, and reset shared cart state after success.
9. Update [styles.css](/d:/shoplite/frontend/src/styles.css) for header, cart badge, cart layout, totals panel, checkout actions, and empty states.
10. Touch [index.css](/d:/shoplite/frontend/src/index.css) only if global shell spacing needs to move off `body` to support the new header/app shell.

**Wiring**
1. Use a backend-generated anonymous `cart_id` cookie end to end. The backend should create and set it when absent; the frontend should rely on normal browser cookie handling rather than local storage or a frontend UUID.
2. Keep cross-module boundaries strict: `orders.service` may call `cart.service`, but must not call `cart.repository` directly.
3. Keep this lab scoped to the requested surface only: no backend `checkout/` module, no tests, no order-history page, no auth, no payment flow.
4. Treat cart quantity editing as limited in this lab because the requested API surface does not include PATCH/PUT. Repeated adds can increment quantity; cart page supports remove.

**Relevant Existing Files**
- [backend/app/main.py](/d:/shoplite/backend/app/main.py) for router registration
- [backend/app/core/errors.py](/d:/shoplite/backend/app/core/errors.py) for error shape reuse
- [backend/app/modules/catalog/router.py](/d:/shoplite/backend/app/modules/catalog/router.py) as the router template
- [backend/app/modules/catalog/service.py](/d:/shoplite/backend/app/modules/catalog/service.py) as the thin service template
- [backend/app/modules/catalog/repository.py](/d:/shoplite/backend/app/modules/catalog/repository.py) as the repository template
- [backend/alembic/versions/ad76914b8a3b_initial_catalog_tables.py](/d:/shoplite/backend/alembic/versions/ad76914b8a3b_initial_catalog_tables.py) as the migration template
- [frontend/src/App.tsx](/d:/shoplite/frontend/src/App.tsx) for route and shell wiring
- [frontend/src/api/catalog.ts](/d:/shoplite/frontend/src/api/catalog.ts) for API-client style
- [frontend/src/pages/ProductDetailPage.tsx](/d:/shoplite/frontend/src/pages/ProductDetailPage.tsx) for the add-to-cart entry point
- [frontend/src/styles.css](/d:/shoplite/frontend/src/styles.css) for the new UI sections

**Verification**
1. Run `alembic upgrade head` and confirm the four new tables and constraints exist.
2. Manually exercise `GET /api/cart`, `POST /api/cart/items`, `DELETE /api/cart/items/{product_id}`, and `POST /api/orders` to confirm cookie creation, totals, order creation, and cart clearing.
3. Run the frontend and verify add-to-cart from product detail, header count updates, `/cart` remove flow, `/checkout` empty-cart blocking, and successful checkout resetting the cart count.
4. Smoke-check that existing catalog pages still work against the unchanged catalog endpoints.

This plan is saved in session memory at `/memories/session/plan.md`. If you want, the next step is either:
1. Approve this plan for handoff and implementation.
2. Ask me to revise the plan for a different cart UX, such as quantity increment/decrement controls.
