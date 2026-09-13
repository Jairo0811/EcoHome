type Props = { status: 'ONLINE' | 'OFFLINE' | 'WARNING' };

const labels = {
  ONLINE: 'En línea',
  OFFLINE: 'Fuera de línea',
  WARNING: 'Advertencia',
} as const;

export function DeviceStatus({ status }: Props) {
  return <span className={`device-status status-${status.toLowerCase()}`}>{labels[status]}</span>;
}
