import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleCheck, faRotate, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

import { useOperations } from '../hooks/useOperations';

export function OperationsOverview() {
  const { alerts, rules, error, resolve, execute } = useOperations();

  return (
    <>
      <article className="panel devices-panel" id="alertas">
        <div className="panel-heading">
          <div><p className="eyebrow">Alertas</p><h3>Situaciones que requieren atención</h3></div>
          <span className="device-count">{alerts.length}</span>
        </div>

        {error && <p className="subtitle">{error}</p>}

        {alerts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon"><FontAwesomeIcon icon={faCircleCheck} /></div>
            <strong>Todo en orden</strong>
            <p>No hay alertas abiertas.</p>
          </div>
        ) : (
          <div className="device-list">
            {alerts.slice(0, 5).map((alert) => (
              <div className="device-row" key={alert.id}>
                <div className="device-icon"><FontAwesomeIcon icon={faTriangleExclamation} /></div>
                <div className="device-copy">
                  <strong>{alert.title}</strong>
                  <span>{alert.message}</span>
                </div>
                <button className="secondary-button" type="button" onClick={() => void resolve(alert.id)}>Resolver</button>
              </div>
            ))}
          </div>
        )}
      </article>

      <article className="panel devices-panel" id="automatizaciones">
        <div className="panel-heading">
          <div><p className="eyebrow">Automatización</p><h3>Reglas inteligentes</h3></div>
          <span className="device-count">{rules.filter((rule) => rule.enabled).length}</span>
        </div>

        {rules.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon"><FontAwesomeIcon icon={faRotate} /></div>
            <strong>Sin reglas todavía</strong>
            <p>Las automatizaciones configuradas aparecerán aquí.</p>
          </div>
        ) : (
          <div className="device-list">
            {rules.slice(0, 5).map((rule) => (
              <div className="device-row" key={rule.id}>
                <div className="device-icon"><FontAwesomeIcon icon={faRotate} /></div>
                <div className="device-copy">
                  <strong>{rule.name}</strong>
                  <span>{rule.trigger_type} → {rule.action_type}</span>
                </div>
                <button className="secondary-button" type="button" disabled={!rule.enabled} onClick={() => void execute(rule.id)}>Ejecutar</button>
              </div>
            ))}
          </div>
        )}
      </article>
    </>
  );
}
