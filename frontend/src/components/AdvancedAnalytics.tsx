import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine } from '@fortawesome/free-solid-svg-icons';

import { useReports } from '../hooks/useReports';

const max = (values: number[]) => Math.max(...values, 1);

export function AdvancedAnalytics() {
  const { data, error } = useReports();

  if (error) {
    return <article className="panel" id="reportes"><p className="subtitle">{error}</p></article>;
  }

  if (!data) {
    return <article className="panel" id="reportes"><p className="subtitle">Cargando analítica…</p></article>;
  }

  const energy = data.trends.ENERGY_KWH;
  const peak = max(energy.map((item) => item.total));

  return (
    <article className="panel consumption-panel analytics-panel" id="reportes">
      <div className="panel-heading">
        <div><p className="eyebrow">Analítica · 30 días</p><h3>Rendimiento del hogar</h3></div>
        <span className="period-chip"><FontAwesomeIcon icon={faChartLine} /> {data.periodDays} días</span>
      </div>

      <div className="analytics-kpis">
        <div><strong>{data.alerts.open}</strong><span>alertas abiertas</span></div>
        <div><strong>{data.securityEvents}</strong><span>eventos de seguridad</span></div>
        <div><strong>{data.automationExecutions}</strong><span>automatizaciones</span></div>
      </div>

      <div className="resource-list analytics-trend">
        <strong>Tendencia de energía</strong>
        {energy.length === 0 ? (
          <p className="subtitle">Sin datos históricos.</p>
        ) : (
          <div className="energy-bars" aria-label="Tendencia de consumo energético">
            {energy.map((point) => (
              <span
                key={point.date}
                title={`${point.date}: ${point.total} kWh`}
                style={{ height: `${Math.max((point.total / peak) * 100, 4)}%` }}
              />
            ))}
          </div>
        )}
      </div>
    </article>
  );
}
