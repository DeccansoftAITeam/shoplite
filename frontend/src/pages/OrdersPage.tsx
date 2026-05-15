import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getErrorMessage } from '../api/client';
import { fetchOrders, type OrderSummary } from '../api/orders';

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<OrderSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOrders()
      .then(setOrders)
      .catch((requestError) => {
        setError(getErrorMessage(requestError, 'Failed to load orders.'));
      })
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <p className="status">Loading orders…</p>;
  }

  if (error) {
    return <p className="status error">{error}</p>;
  }

  if (orders.length === 0) {
    return (
      <main className="page-shell page-panel empty-state">
        <h1>No orders yet</h1>
        <p>Complete checkout once and your order history will appear here.</p>
        <Link to="/" className="primary-button inline-action">
          Browse products
        </Link>
      </main>
    );
  }

  return (
    <main className="page-shell orders-page">
      <section className="page-panel page-title-row">
        <div>
          <p className="eyebrow">Orders</p>
          <h1>Past orders</h1>
        </div>
        <p className="cart-summary-pill">{orders.length} total orders</p>
      </section>

      <section className="page-panel orders-list">
        {orders.map((order) => (
          <Link key={order.id} to={`/orders/${order.id}`} className="order-card">
            <div>
              <p className="eyebrow">Order #{order.id}</p>
              <h2>{formatDate(order.created_at)}</h2>
            </div>
            <div className="order-card-meta">
              <p className="order-status">{order.status}</p>
              <p className="price">${Number(order.total_amount).toFixed(2)}</p>
            </div>
          </Link>
        ))}
      </section>
    </main>
  );
}