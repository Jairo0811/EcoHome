import { useState } from 'react';

const navigation = [
  { icon: '⌂', label: 'Inicio', target: 'inicio' },
  { icon: '◉', label: 'Dispositivos', target: 'dispositivos' },
  { icon: '↯', label: 'Consumo', target: 'consumo' },
  { icon: '◇', label: 'Seguridad', target: 'seguridad' },
  { icon: '⚙', label: 'Automatizaciones', target: 'automatizaciones' },
  { icon: '!', label: 'Alertas', target: 'alertas' },
  { icon: '▤', label: 'Reportes', target: 'reportes' },
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
        <div className="brand-mark" aria-hidden="true">⌂</div>
        <div>
          <span className="brand-eco">Eco</span>
          <span className="brand-home">Home</span>
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
            >
              <span className="nav-icon" aria-hidden="true">{icon}</span>
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
