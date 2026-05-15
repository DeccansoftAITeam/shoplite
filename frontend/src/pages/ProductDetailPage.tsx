import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getErrorMessage } from '../api/client';
import { fetchProduct, type Product } from '../api/catalog';
import { useCart } from '../context/CartContext';

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);
  const [cartMessage, setCartMessage] = useState<string | null>(null);
  const { addItem } = useCart();

  useEffect(() => {
    if (!id) {
      setError('Invalid product ID.');
      setLoading(false);
      return;
    }
    fetchProduct(Number(id))
      .then(setProduct)
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load product.');
      })
      .finally(() => setLoading(false));
  }, [id]);

  async function handleAddToCart() {
    if (!product) {
      return;
    }

    try {
      setIsAdding(true);
      setCartMessage(null);
      await addItem(product.id, 1);
      setCartMessage(`${product.name} added to cart.`);
    } catch (requestError) {
      setCartMessage(getErrorMessage(requestError, 'Unable to add item to cart.'));
    } finally {
      setIsAdding(false);
    }
  }

  if (loading) return <p className="status">Loading…</p>;
  if (error) return <p className="status error">{error}</p>;
  if (!product) return null;

  return (
    <main className="page-shell product-detail page-panel">
      <Link to="/" className="back-link">← Back to Products</Link>
      <h1>{product.name}</h1>
      {product.description && <p>{product.description}</p>}
      <p className="price">${Number(product.price).toFixed(2)}</p>
      <p className="stock">In stock: {product.stock}</p>
      <div className="detail-actions">
        <button
          type="button"
          className="primary-button"
          onClick={() => void handleAddToCart()}
          disabled={product.stock === 0 || isAdding}
        >
          {product.stock === 0 ? 'Out of stock' : isAdding ? 'Adding…' : 'Add to cart'}
        </button>
        <Link to="/cart" className="secondary-link">
          View cart
        </Link>
      </div>
      {cartMessage ? <p className="status success detail-status">{cartMessage}</p> : null}
    </main>
  );
}
