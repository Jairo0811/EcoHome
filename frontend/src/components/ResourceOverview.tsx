import { useResources } from '../hooks/useResources';
import type { ResourceMetric } from '../types/resources';

const resources: Array<{ metric: ResourceMetric; label: string; unit: string; symbol: string }> = [
  { metric: 'ENERGY_KWH', label: 'Energía', unit: 'kWh', symbol: '⚡' },
  { metric: 'WATER_L', label: 'Agua', unit: 'L', symbol: '◌' },
  { metric: 'GAS_M3', label: 'Gas', unit: 'm³', symbol: '◈' },
];

export function ResourceOverview() {
  const { data, error } = useResources();
  return (
    <article className="panel consumption-panel">
      <div className="panel-heading"><div><p className="eyebrow">Eficiencia</p><h3>Límites de consumo diario</h3></div><span className="period-chip">Hoy</span></div>
      {error && <p className="subtitle">{error}</p>}
      <div className="resource-list">
        {resources.map(({ metric, label, unit, symbol }) => {
          const item = data?.resources[metric];
          const progress = Math.min(item?.progressPercent ?? 0, 100);
          return <div key={metric}>
            <div className="resource-row"><div className="resource-label"><span className="resource-symbol">{symbol}</span><span>{label}</span></div><strong>{(item?.total ?? 0).toLocaleString('es-DO')} {unit}{item?.limit ? ` / ${item.limit.toLocaleString('es-DO')} ${unit}` : ''}</strong></div>
            <div className="resource-bar"><span style={{ width: `${progress}%` }} /></div>
          </div>;
        })}
      </div>
    </article>
  );
}
