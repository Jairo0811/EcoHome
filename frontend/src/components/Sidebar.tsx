import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBolt,
  faChartLine,
  faGear,
  faHouse,
  faMicrochip,
  faShieldHalved,
  faTriangleExclamation,
} from '@fortawesome/free-solid-svg-icons';

const navigation = [
  { icon: faHouse, label: 'Inicio', target: 'inicio' },
  { icon: faMicrochip, label: 'Dispositivos', target: 'dispositivos' },
  { icon: faBolt, label: 'Consumo', target: 'consumo' },
  { icon: faShieldHalved, label: 'Seguridad', target: 'seguridad' },
  { icon: faGear, label: 'Automatizaciones', target: 'automatizaciones' },
  { icon: faTriangleExclamation, label: 'Alertas', target: 'alertas' },
  { icon: faChartLine, label: 'Reportes', target: 'reportes' },
] as const;

export function Sidebar() {
  const [activeTarget, setActiveTarget] = useState('inicio');

  function navigateTo(target: string) {
    const destination = document.getElementById(target);
    if (!destination) return;

    setActiveTarget(target);
    destination.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark" aria-hidden="true">
          <img src="/favicon.png" alt="" className="brand-isotipo" />
        </div>
        <div className="brand-copy">
          <div>
            <span className="brand-eco">Eco</span>
            <span className="brand-home">Home</span>
          </div>
          <small>Smart Living</small>
        </div>
      </div>

      <nav className="navigation" aria-label="Navegación principal">
        {navigation.map(({ icon, label, target }) => {
          const active = activeTarget === target;
          return (
            <button
              className={`nav-item ${active ? 'active' : ''}`}
              key={target}
              type="button"
              onClick={() => navigateTo(target)}
              aria-current={active ? 'page' : undefined}
              title={label}
            >
              <span className="nav-icon" aria-hidden="true">
                <FontAwesomeIcon icon={icon} />
              </span>
              <span>{label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <span className="status-dot" />
        <span>EcoHome 1.1.0</span>
      </div>
    </aside>
  );
}
