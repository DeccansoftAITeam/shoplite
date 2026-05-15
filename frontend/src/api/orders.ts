import { apiClient } from './client';

export interface PlacedOrder {
  id: number;
  status: string;
  total_amount: string;
  created_at: string;
}

export async function placeOrder(): Promise<PlacedOrder> {
  const { data } = await apiClient.post<PlacedOrder>('/api/orders');
  return data;
}