import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getErrorMessage } from '../api/client';
import { placeOrder } from '../api/orders';
import { useCart } from '../context/CartContext';

export default function CheckoutPage() {
  const { cart, error, isLoading, refreshCart } = useCart();
  const navigate = useNavigate();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleCheckout() {
    try {
      setIsSubmitting(true);
      setSubmitError(null);
      const order = await placeOrder();
      await refreshCart();
      navigate('/cart', {
        state: {
          message: `Order #${order.id} placed for $${Number(order.total_amount).toFixed(2)}.`,
        },
      });
    } catch (requestError) {
      setSubmitError(getErrorMessage(requestError, 'Checkout failed.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return <p className="status">Loading checkout…</p>;
  }

  if (error && cart === null) {
    return <p className="status error">{error}</p>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <main className="page-shell page-panel empty-state">
        <h1>Nothing to checkout yet</h1>
        <p>Add at least one item before placing an order.</p>
        <Link to="/" className="primary-button inline-action">
          Browse products
        </Link>
      </main>
    );
  }

  return (
    <main className="page-shell checkout-page">
      <section className="page-panel page-title-row">
        <div>
          <p className="eyebrow">Checkout</p>
          <h1>Review and place order</h1>
        </div>
        <Link to="/cart" className="secondary-link">
          Back to cart
        </Link>
      </section>

      {submitError ? <p className="status error">{submitError}</p> : null}

      <section className="checkout-layout">
        <div className="page-panel cart-list">
          {cart.items.map((item) => (
            <article key={item.product_id} className="cart-row checkout-row">
              <div>
                <h2>{item.name}</h2>
                <p className="line-meta">Quantity {item.quantity}</p>
              </div>
              <p className="price">${Number(item.line_total).toFixed(2)}</p>
            </article>
          ))}
        </div>

        <aside className="page-panel order-summary">
          <p className="eyebrow">Order total</p>
          <div className="summary-row">
            <span>Items</span>
            <strong>{cart.total_quantity}</strong>
          </div>
          <div className="summary-row total-row">
            <span>Total</span>
            <strong>${Number(cart.total_amount).toFixed(2)}</strong>
          </div>
          <button
            type="button"
            className="primary-button full-width-button"
            onClick={() => void handleCheckout()}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Placing order…' : 'Place order'}
          </button>
        </aside>
      </section>
    </main>
  );
}