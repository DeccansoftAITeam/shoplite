import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getErrorMessage } from '../api/client';
import { fetchOrder, type OrderDetail } from '../api/orders';

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    setError(null);

    if (!id) {
      setOrder(null);
      setError('Invalid order ID.');
      setIsLoading(false);
      return;
    }

    const orderId = Number(id);

    if (!Number.isInteger(orderId) || orderId <= 0) {
      setOrder(null);
      setError('Invalid order ID.');
      setIsLoading(false);
      return;
    }

    fetchOrder(orderId)
      .then(setOrder)
      .catch((requestError) => {
        setError(getErrorMessage(requestError, 'Failed to load order.'));
      })
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) {
    return <p className="status">Loading order…</p>;
  }

  if (error) {
    return <p className="status error">{error}</p>;
  }

  if (!order) {
    return null;
  }

  return (
    <main className="page-shell orders-page">
      <section className="page-panel page-title-row">
        <div>
          <p className="eyebrow">Order #{order.id}</p>
          <h1>Order details</h1>
          <p className="muted-copy">Placed {formatDate(order.created_at)}</p>
        </div>
        <Link to="/orders" className="secondary-link">
          Back to orders
        </Link>
      </section>

      <section className="order-detail-layout">
        <div className="page-panel orders-list">
          {order.items.map((item) => (
            <article key={`${item.product_id}-${item.product_name}`} className="cart-row checkout-row">
              <div>
                <h2>{item.product_name}</h2>
                <p className="line-meta">Quantity {item.quantity}</p>
                <p className="muted-copy">Unit price ${Number(item.unit_price).toFixed(2)}</p>
              </div>
              <p className="price">${Number(item.line_total).toFixed(2)}</p>
            </article>
          ))}
        </div>

        <aside className="page-panel order-summary">
          <p className="eyebrow">Summary</p>
          <div className="summary-row">
            <span>Status</span>
            <strong>{order.status}</strong>
          </div>
          <div className="summary-row total-row">
            <span>Total</span>
            <strong>${Number(order.total_amount).toFixed(2)}</strong>
          </div>
        </aside>
      </section>
    </main>
  );
}