import { useEffect, useState } from 'react';

import { api } from '../api/http';
import type { DashboardSummary } from '../types/dashboard';

interface DashboardState { data: DashboardSummary | null; loading: boolean; error: string | null; }

export function useDashboard(): DashboardState {
  const [state, setState] = useState<DashboardState>({ data: null, loading: true, error: null });

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const data = await api.getDashboardSummary();
        if (active) setState({ data, loading: false, error: null });
      } catch (error: unknown) {
        if (active) setState((current) => ({ data: current.data, loading: false, error: error instanceof Error ? error.message : 'No se pudo conectar con la API.' }));
      }
    }
    void load();
    const timer = window.setInterval(() => void load(), 5000);
    return () => { active = false; window.clearInterval(timer); };
  }, []);

  return state;
}
