import type { AuthTokens, AuthUser } from '../types/auth';
import type { DashboardSummary } from '../types/dashboard';
import type { IotConfig, IotTopic } from '../types/iot';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1';
const ACCESS_KEY = 'ecohome.access';
const REFRESH_KEY = 'ecohome.refresh';
export const tokenStore = { getAccess:()=>localStorage.getItem(ACCESS_KEY), getRefresh:()=>localStorage.getItem(REFRESH_KEY), set(tokens:AuthTokens){localStorage.setItem(ACCESS_KEY,tokens.access);localStorage.setItem(REFRESH_KEY,tokens.refresh)}, clear(){localStorage.removeItem(ACCESS_KEY);localStorage.removeItem(REFRESH_KEY)} };
async function request<T>(path:string, init:RequestInit={}, authenticated=true):Promise<T>{const headers=new Headers(init.headers);headers.set('Accept','application/json');if(init.body)headers.set('Content-Type','application/json');if(authenticated){const access=tokenStore.getAccess();if(access)headers.set('Authorization',`Bearer ${access}`)}const response=await fetch(`${API_BASE_URL}${path}`,{...init,headers});if(!response.ok)throw new Error(`EcoHome API respondió con estado ${response.status}`);if(response.status===204)return undefined as T;return response.json() as Promise<T>}
export const api={
  login:(username:string,password:string)=>request<AuthTokens>('/auth/token/',{method:'POST',body:JSON.stringify({username,password})},false),
  register:(payload:{username:string;email:string;password:string})=>request<AuthUser>('/auth/register/',{method:'POST',body:JSON.stringify(payload)},false),
  getMe:()=>request<AuthUser>('/auth/me/'),
  getDashboardSummary:()=>request<DashboardSummary>('/dashboard/summary/'),
  getIotConfig:()=>request<IotConfig>('/iot/config/'),
  getIotTopics:()=>request<IotTopic[]>('/iot/topics/'),
  ingest:(externalId:string,payload:unknown)=>request(`/iot/ingest/${encodeURIComponent(externalId)}/`,{method:'POST',body:JSON.stringify(payload)}),
  sendDeviceCommand:(deviceId:number,payload:unknown)=>request(`/iot/devices/${deviceId}/command/`,{method:'POST',body:JSON.stringify(payload)}),
};
