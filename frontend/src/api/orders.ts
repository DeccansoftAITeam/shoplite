import { apiClient } from './client';

export interface OrderSummary {
  id: number;
  status: string;
  total_amount: string;
  created_at: string;
}

export interface OrderItem {
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: string;
  line_total: string;
}

export interface OrderDetail extends OrderSummary {
  items: OrderItem[];
}

export type PlacedOrder = OrderSummary;

export async function fetchOrders(): Promise<OrderSummary[]> {
  const { data } = await apiClient.get<OrderSummary[]>('/api/orders');
  return data;
}

export async function fetchOrder(orderId: number): Promise<OrderDetail> {
  const { data } = await apiClient.get<OrderDetail>(`/api/orders/${orderId}`);
  return data;
}

export async function placeOrder(): Promise<PlacedOrder> {
  const { data } = await apiClient.post<PlacedOrder>('/api/orders');
  return data;
}