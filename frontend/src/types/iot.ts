export type IotTopic = { deviceId: number; externalId: string; telemetryTopic: string; commandTopic: string };
export type IotConfig = { host: string; port: number; tls: boolean; username: string };
