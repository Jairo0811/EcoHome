import { useCallback, useEffect, useState } from 'react';

import { api } from '../api/http';
import type { Alert, AutomationRule } from '../types/automation';

export function useOperations() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [rules, setRules] = useState<AutomationRule[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const [alertData, ruleData] = await Promise.all([api.getAlerts(), api.getAutomationRules()]);
      setAlerts(alertData.results);
      setRules(ruleData.results);
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudieron cargar alertas y automatizaciones.');
    }
  }, []);

  useEffect(() => { void load(); const timer=window.setInterval(()=>void load(),10000); return()=>window.clearInterval(timer); }, [load]);

  async function resolve(id:number){await api.resolveAlert(id);await load();}
  async function execute(id:number){await api.executeAutomation(id);await load();}
  return { alerts, rules, error, resolve, execute };
}
