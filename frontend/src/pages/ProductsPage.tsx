import { useEffect, useState } from 'react';
import { fetchProducts, type Product } from '../api/catalog';
import ProductCard from '../components/ProductCard';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load products.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="status">Loading…</p>;
  if (error) return <p className="status error">{error}</p>;

  return (
    <main>
      <h1>Products</h1>
      <div className="product-grid">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </main>
  );
}
