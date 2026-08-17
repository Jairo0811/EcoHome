import { useEffect, useState } from 'react';

import { api } from '../api/http';
import type { DashboardSummary } from '../types/dashboard';

interface DashboardState {
  data: DashboardSummary | null;
  loading: boolean;
  error: string | null;
}

export function useDashboard(): DashboardState {
  const [state, setState] = useState<DashboardState>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let active = true;

    api.getDashboardSummary()
      .then((data) => {
        if (active) {
          setState({ data, loading: false, error: null });
        }
      })
      .catch((error: unknown) => {
        if (active) {
          const message = error instanceof Error ? error.message : 'No se pudo conectar con la API.';
          setState({ data: null, loading: false, error: message });
        }
      });

    return () => {
      active = false;
    };
  }, []);

  return state;
}
