import { useCallback, useEffect, useState } from 'react';

import { api, tokenStore } from '../api/http';
import type { AuthUser } from '../types/auth';

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadUser = useCallback(async () => {
    if (!tokenStore.getAccess()) {
      setLoading(false);
      return;
    }
    try {
      setUser(await api.getMe());
    } catch {
      tokenStore.clear();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void loadUser(); }, [loadUser]);

  async function login(username: string, password: string) {
    setError(null);
    try {
      const tokens = await api.login(username, password);
      tokenStore.set(tokens);
      setUser(await api.getMe());
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo iniciar sesión.');
      throw cause;
    }
  }

  function logout() {
    tokenStore.clear();
    setUser(null);
  }

  return { user, loading, error, login, logout };
}
