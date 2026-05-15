import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { addCartItem, fetchCart, removeCartItem, type Cart } from '../api/cart';
import { getErrorMessage } from '../api/client';

interface CartContextValue {
  cart: Cart | null;
  error: string | null;
  isLoading: boolean;
  itemCount: number;
  addItem: (productId: number, quantity?: number) => Promise<Cart>;
  refreshCart: () => Promise<Cart>;
  removeItem: (productId: number) => Promise<Cart>;
}

const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const hasLoaded = useRef(false);

  async function refreshCart(): Promise<Cart> {
    try {
      const nextCart = await fetchCart();
      setCart(nextCart);
      setError(null);
      return nextCart;
    } catch (requestError) {
      const message = getErrorMessage(requestError, 'Failed to load cart.');
      setError(message);
      throw requestError;
    } finally {
      setIsLoading(false);
    }
  }

  async function addItem(productId: number, quantity = 1): Promise<Cart> {
    try {
      const nextCart = await addCartItem(productId, quantity);
      setCart(nextCart);
      setError(null);
      return nextCart;
    } catch (requestError) {
      const message = getErrorMessage(requestError, 'Failed to add item to cart.');
      setError(message);
      throw requestError;
    }
  }

  async function removeItem(productId: number): Promise<Cart> {
    try {
      const nextCart = await removeCartItem(productId);
      setCart(nextCart);
      setError(null);
      return nextCart;
    } catch (requestError) {
      const message = getErrorMessage(requestError, 'Failed to remove item from cart.');
      setError(message);
      throw requestError;
    }
  }

  useEffect(() => {
    if (hasLoaded.current) {
      return;
    }

    hasLoaded.current = true;
    void refreshCart();
  }, []);

  return (
    <CartContext.Provider
      value={{
        cart,
        error,
        isLoading,
        itemCount: cart?.total_quantity ?? 0,
        addItem,
        refreshCart,
        removeItem,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart(): CartContextValue {
  const context = useContext(CartContext);
  if (context === null) {
    throw new Error('useCart must be used inside CartProvider.');
  }

  return context;
}