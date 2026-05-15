import { NavLink } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Header() {
  const { itemCount } = useCart();

  return (
    <header className="site-header">
      <div>
        <p className="eyebrow">ShopLite</p>
        <NavLink to="/" className="brand-link">
          Everyday essentials, fast checkout.
        </NavLink>
      </div>
      <nav className="site-nav" aria-label="Primary">
        <NavLink to="/" className="nav-link">
          Products
        </NavLink>
        <NavLink to="/cart" className="nav-link cart-link">
          Cart
          <span className="cart-count" aria-label={`${itemCount} items in cart`}>
            {itemCount}
          </span>
        </NavLink>
      </nav>
    </header>
  );
}