import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLightbulb, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

import { useRecommendations } from '../hooks/useRecommendations';

export function RecommendationsOverview() {
  const { items, dismiss, apply } = useRecommendations();

  return (
    <article className="panel devices-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">EcoHome Insights</p><h3>Recomendaciones inteligentes</h3></div>
        <span className="device-count">{items.length}</span>
      </div>

      {items.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon"><FontAwesomeIcon icon={faLightbulb} /></div>
          <strong>Sin recomendaciones pendientes</strong>
          <p>Tu hogar no requiere ajustes destacados en este momento.</p>
        </div>
      ) : (
        <div className="device-list">
          {items.slice(0, 5).map((item) => (
            <div className="device-row" key={item.id}>
              <div className="device-icon">
                <FontAwesomeIcon icon={item.priority === 'HIGH' ? faTriangleExclamation : faLightbulb} />
              </div>
              <div className="device-copy">
                <strong>{item.title}</strong>
                <span>{item.description}{item.estimated_savings_percent ? ` · ahorro estimado ${item.estimated_savings_percent}%` : ''}</span>
              </div>
              <div className="hero-actions">
                <button className="secondary-button" onClick={() => void dismiss(item.id)}>Descartar</button>
                <button className="primary-button" onClick={() => void apply(item.id)}>Aplicada</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </article>
  );
}
