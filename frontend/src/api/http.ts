import type { DashboardSummary } from '../types/dashboard';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1';

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Accept: 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`EcoHome API respondió con estado ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  getDashboardSummary: () => request<DashboardSummary>('/dashboard/summary/'),
};
