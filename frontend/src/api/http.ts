import type { Alert, AutomationRule, Paginated } from '../types/automation';
import type { AuthTokens, AuthUser } from '../types/auth';
import type { DashboardSummary } from '../types/dashboard';
import type { IotConfig, IotTopic } from '../types/iot';
import type { Recommendation } from '../types/recommendations';
import type { ReportOverview } from '../types/reports';
import type { ResourceHistory, ResourceMetric, ResourceSummary } from '../types/resources';
import type { SecurityEvent, SecurityMode, SecurityState } from '../types/security';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1';
const ACCESS_KEY = 'ecohome.access';
const REFRESH_KEY = 'ecohome.refresh';

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set(tokens: AuthTokens) {
    localStorage.setItem(ACCESS_KEY, tokens.access);
    localStorage.setItem(REFRESH_KEY, tokens.refresh);
  },
  clear() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

async function request<T>(path: string, init: RequestInit = {}, auth = true): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body) headers.set('Content-Type', 'application/json');

  if (auth) {
    const access = tokenStore.getAccess();
    if (access) headers.set('Authorization', `Bearer ${access}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });

  if (!response.ok) {
    if (path === '/auth/token/' && response.status === 401) {
      throw new Error('Usuario o contraseña incorrectos.');
    }

    let message = `EcoHome API respondió con estado ${response.status}`;
    try {
      const payload = await response.clone().json() as { detail?: unknown };
      if (typeof payload.detail === 'string' && payload.detail.trim()) {
        message = payload.detail;
      }
    } catch {
      // Mantener el mensaje genérico si la respuesta no contiene JSON utilizable.
    }
    throw new Error(message);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  login: (username: string, password: string) =>
    request<AuthTokens>(
      '/auth/token/',
      { method: 'POST', body: JSON.stringify({ username, password }) },
      false,
    ),
  register: (payload: { username: string; email: string; password: string }) =>
    request<AuthUser>('/auth/register/', { method: 'POST', body: JSON.stringify(payload) }, false),
  getMe: () => request<AuthUser>('/auth/me/'),
  getDashboardSummary: () => request<DashboardSummary>('/dashboard/summary/'),
  getIotConfig: () => request<IotConfig>('/iot/config/'),
  getIotTopics: () => request<IotTopic[]>('/iot/topics/'),
  ingest: (externalId: string, payload: unknown) =>
    request(`/iot/ingest/${encodeURIComponent(externalId)}/`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  sendDeviceCommand: (id: number, payload: unknown) =>
    request(`/iot/devices/${id}/command/`, { method: 'POST', body: JSON.stringify(payload) }),
  getResourceSummary: (range: 'day' | 'week' | 'month' = 'day') =>
    request<ResourceSummary>(`/resources/summary/?range=${range}`),
  getResourceHistory: (metric: ResourceMetric, days = 30) =>
    request<ResourceHistory>(`/resources/history/?metric=${metric}&days=${days}`),
  getAlerts: () => request<Paginated<Alert>>('/automation/alerts/?status=OPEN'),
  resolveAlert: (id: number) => request<Alert>(`/automation/alerts/${id}/resolve/`, { method: 'POST' }),
  getAutomationRules: () => request<Paginated<AutomationRule>>('/automation/rules/'),
  executeAutomation: (id: number) => request(`/automation/rules/${id}/execute/`, { method: 'POST' }),
  getSecurityStates: () => request<SecurityState[]>('/security/states/'),
  setSecurityMode: (home: number, mode: SecurityMode) =>
    request<SecurityState>(`/security/states/${home}/`, {
      method: 'PATCH',
      body: JSON.stringify({ mode }),
    }),
  getSecurityEvents: () => request<Paginated<SecurityEvent>>('/security/events/'),
  getReportOverview: (days = 30) => request<ReportOverview>(`/reports/overview/?days=${days}`),
  getRecommendations: () => request<Paginated<Recommendation>>('/recommendations/'),
  refreshRecommendations: () =>
    request<Recommendation[]>('/recommendations/refresh/', { method: 'POST' }),
  dismissRecommendation: (id: number) =>
    request<Recommendation>(`/recommendations/${id}/dismiss/`, { method: 'POST' }),
  applyRecommendation: (id: number) =>
    request<Recommendation>(`/recommendations/${id}/apply/`, { method: 'POST' }),
  runSimulation: (steps = 10) =>
    request<{ home: number; steps: number; telemetryCreated: number; telemetryIds: number[] }>(
      '/simulator/run/',
      { method: 'POST', body: JSON.stringify({ steps }) },
    ),
};
