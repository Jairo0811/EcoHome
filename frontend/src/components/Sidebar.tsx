const navigation = [
  ['⌂', 'Inicio'],
  ['⌁', 'Mi hogar'],
  ['▦', 'Habitaciones'],
  ['◉', 'Dispositivos'],
  ['↯', 'Consumo'],
  ['◇', 'Seguridad'],
  ['⚙', 'Automatizaciones'],
  ['!', 'Alertas'],
  ['▤', 'Reportes'],
];

export function Sidebar() {
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
        {navigation.map(([icon, label], index) => (
          <button className={`nav-item ${index === 0 ? 'active' : ''}`} key={label} type="button">
            <span className="nav-icon" aria-hidden="true">{icon}</span>
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="status-dot" />
        <span>EcoHome 0.1.0</span>
      </div>
    </aside>
  );
}
