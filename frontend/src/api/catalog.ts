import { apiClient } from './client';

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: string;
  stock: number;
}

export async function fetchProducts(): Promise<Product[]> {
  const { data } = await apiClient.get<Product[]>('/api/catalog/products');
  return data;
}

export async function fetchProduct(id: number): Promise<Product> {
  const { data } = await apiClient.get<Product>(`/api/catalog/products/${id}`);
  return data;
}
