import axios from 'axios';

const baseURL =
  (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL,
  withCredentials: true,
});

interface ApiErrorResponse {
  error?: {
    message?: string;
  };
}

export function getErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    return error.response?.data?.error?.message ?? error.message ?? fallback;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return fallback;
}