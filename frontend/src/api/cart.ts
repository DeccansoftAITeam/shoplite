import { apiClient } from './client';

export interface CartLine {
  product_id: number;
  name: string;
  description: string | null;
  quantity: number;
  stock: number;
  unit_price: string;
  line_total: string;
}

export interface Cart {
  cart_id: string;
  items: CartLine[];
  total_quantity: number;
  total_amount: string;
}

interface AddCartItemPayload {
  product_id: number;
  quantity: number;
}

export async function fetchCart(): Promise<Cart> {
  const { data } = await apiClient.get<Cart>('/api/cart');
  return data;
}

export async function addCartItem(productId: number, quantity = 1): Promise<Cart> {
  const payload: AddCartItemPayload = { product_id: productId, quantity };
  const { data } = await apiClient.post<Cart>('/api/cart/items', payload);
  return data;
}

export async function removeCartItem(productId: number): Promise<Cart> {
  const { data } = await apiClient.delete<Cart>(`/api/cart/items/${productId}`);
  return data;
}