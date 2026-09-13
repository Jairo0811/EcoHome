import { useSecurity } from '../hooks/useSecurity';

export function SecurityOverview() {
  const { states, events, error, setMode } = useSecurity();
  const state = states[0];

  return (
    <article className="panel devices-panel" id="seguridad">
      <div className="panel-heading">
        <div><p className="eyebrow">Seguridad inteligente</p><h3>Protección del hogar</h3></div>
        <span className="period-chip">{state?.mode ?? 'SIN CONFIGURAR'}</span>
      </div>

      {state && (
        <div className="hero-actions">
          <button className="secondary-button" onClick={() => void setMode(state.home, 'DISARMED')}>Desarmar</button>
          <button className="secondary-button" onClick={() => void setMode(state.home, 'HOME')}>En casa</button>
          <button className="primary-button" onClick={() => void setMode(state.home, 'AWAY')}>Fuera</button>
        </div>
      )}

      {error && <p className="subtitle">{error}</p>}

      <div className="device-list">
        {events.slice(0, 5).map((event) => (
          <div className="device-row" key={event.id}>
            <div className="device-icon">{event.severity === 'CRITICAL' ? '!' : '⌁'}</div>
            <div className="device-copy">
              <strong>{event.event_type}</strong>
              <span>{event.device_name ?? 'Sistema'} · {event.message || new Date(event.occurred_at).toLocaleString('es-DO')}</span>
            </div>
          </div>
        ))}
        {events.length === 0 && (
          <div className="empty-state">
            <strong>Sin incidentes recientes</strong>
            <p>Los eventos de cámaras y sensores aparecerán aquí.</p>
          </div>
        )}
      </div>
    </article>
  );
}
