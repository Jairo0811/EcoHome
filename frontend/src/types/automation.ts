export type AlertStatus = 'OPEN' | 'ACKNOWLEDGED' | 'RESOLVED';
export type AlertSeverity = 'INFO' | 'WARNING' | 'CRITICAL';
export type Alert = { id:number; home:number; device:number|null; device_name:string|null; alert_type:string; severity:AlertSeverity; status:AlertStatus; title:string; message:string; created_at:string; resolved_at:string|null };
export type AutomationRule = { id:number; home:number; name:string; enabled:boolean; trigger_type:string; trigger_config:Record<string,unknown>; action_type:string; action_config:Record<string,unknown>; last_triggered_at:string|null };
export type Paginated<T> = { count:number; next:string|null; previous:string|null; results:T[] };
