import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getErrorMessage } from '../api/client';
import { useCart } from '../context/CartContext';

interface CartLocationState {
  message?: string;
}

export default function CartPage() {
  const { cart, error, isLoading, removeItem } = useCart();
  const location = useLocation();
  const [removingProductId, setRemovingProductId] = useState<number | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const message = (location.state as CartLocationState | null)?.message ?? null;

  async function handleRemove(productId: number) {
    try {
      setRemovingProductId(productId);
      setActionError(null);
      await removeItem(productId);
    } catch (requestError) {
      setActionError(getErrorMessage(requestError, 'Failed to remove item.'));
    } finally {
      setRemovingProductId(null);
    }
  }

  if (isLoading) {
    return <p className="status">Loading cart…</p>;
  }

  if (error && cart === null) {
    return <p className="status error">{error}</p>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <main className="page-shell page-panel empty-state">
        {message ? <p className="status success">{message}</p> : null}
        <h1>Your cart is empty</h1>
        <p>Add a product to start building an order.</p>
        <Link to="/" className="primary-button inline-action">
          Browse products
        </Link>
      </main>
    );
  }

  return (
    <main className="page-shell cart-page">
      <section className="page-panel page-title-row">
        <div>
          <p className="eyebrow">Cart</p>
          <h1>Your bag</h1>
        </div>
        <p className="cart-summary-pill">{cart.total_quantity} items ready for checkout</p>
      </section>

      {message ? <p className="status success">{message}</p> : null}
      {actionError ? <p className="status error">{actionError}</p> : null}

      <section className="cart-layout">
        <div className="page-panel cart-list">
          {cart.items.map((item) => (
            <article key={item.product_id} className="cart-row">
              <div>
                <h2>{item.name}</h2>
                {item.description ? <p className="muted-copy">{item.description}</p> : null}
                <p className="line-meta">Quantity {item.quantity}</p>
              </div>
              <div className="cart-row-actions">
                <p className="price">${Number(item.line_total).toFixed(2)}</p>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => void handleRemove(item.product_id)}
                  disabled={removingProductId === item.product_id}
                >
                  {removingProductId === item.product_id ? 'Removing…' : 'Remove'}
                </button>
              </div>
            </article>
          ))}
        </div>

        <aside className="page-panel order-summary">
          <p className="eyebrow">Summary</p>
          <div className="summary-row">
            <span>Items</span>
            <strong>{cart.total_quantity}</strong>
          </div>
          <div className="summary-row total-row">
            <span>Total</span>
            <strong>${Number(cart.total_amount).toFixed(2)}</strong>
          </div>
          <Link to="/checkout" className="primary-button full-width-button">
            Continue to checkout
          </Link>
          <p className="muted-copy compact-copy">
            Item quantities increase from the product detail page in this lab scope.
          </p>
        </aside>
      </section>
    </main>
  );
}