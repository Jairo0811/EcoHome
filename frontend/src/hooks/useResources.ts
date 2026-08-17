import { useEffect, useState } from 'react';

import { api } from '../api/http';
import type { ResourceSummary } from '../types/resources';

export function useResources() {
  const [data, setData] = useState<ResourceSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const summary = await api.getResourceSummary('day');
        if (active) { setData(summary); setError(null); }
      } catch (cause) {
        if (active) setError(cause instanceof Error ? cause.message : 'No se pudo cargar el consumo.');
      }
    }
    void load();
    const timer = window.setInterval(() => void load(), 10000);
    return () => { active = false; window.clearInterval(timer); };
  }, []);

  return { data, error };
}
