export type SecurityMode='DISARMED'|'HOME'|'AWAY';
export type SecurityState={id:number;home:number;mode:SecurityMode;updated_at:string};
export type SecurityEvent={id:number;home:number;device:number|null;device_name:string|null;event_type:string;severity:string;message:string;occurred_at:string};
