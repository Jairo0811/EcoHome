import type { DeviceStatus as DeviceStatusValue } from '../types/dashboard';

interface DeviceStatusProps {
  status: DeviceStatusValue;
}

const labels: Record<DeviceStatusValue, string> = {
  ONLINE: 'En línea',
  OFFLINE: 'Fuera de línea',
  WARNING: 'Advertencia',
};

export function DeviceStatus({ status }: DeviceStatusProps) {
  return <span className={`device-status status-${status.toLowerCase()}`}>{labels[status]}</span>;
}
