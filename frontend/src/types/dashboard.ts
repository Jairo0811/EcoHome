export type DeviceStatus = 'ONLINE' | 'OFFLINE' | 'WARNING';

export interface RecentDevice {
  id: number;
  name: string;
  type: string;
  status: DeviceStatus;
  room: string | null;
  lastSeenAt: string | null;
}

export interface DashboardSummary {
  homes: number;
  devices: {
    total: number;
    online: number;
    warning: number;
  };
  consumption24h: {
    energyKwh: number;
    waterLiters: number;
    gasM3: number;
  };
  recentDevices: RecentDevice[];
}
