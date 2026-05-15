import { useNavigate } from 'react-router-dom';
import type { Product } from '../api/catalog';

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  const navigate = useNavigate();

  function handleClick() {
    navigate(`/products/${product.id}`);
  }

  return (
    <div className="product-card" onClick={handleClick} role="button" tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}>
      <h2>{product.name}</h2>
      <p className="price">${Number(product.price).toFixed(2)}</p>
      <p className="stock">In stock: {product.stock}</p>
    </div>
  );
}
