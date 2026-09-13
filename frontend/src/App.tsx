import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBolt,
  faCircleCheck,
  faDroplet,
  faHouse,
  faLeaf,
  faMicrochip,
  faRightFromBracket,
} from '@fortawesome/free-solid-svg-icons';

import { AdvancedAnalytics } from './components/AdvancedAnalytics';
import { DeviceStatus } from './components/DeviceStatus';
import { LoginScreen } from './components/LoginScreen';
import { OperationsOverview } from './components/OperationsOverview';
import { RecommendationsOverview } from './components/RecommendationsOverview';
import { ResourceOverview } from './components/ResourceOverview';
import { SecurityOverview } from './components/SecurityOverview';
import { Sidebar } from './components/Sidebar';
import { SimulatorPanel } from './components/SimulatorPanel';
import { StatCard } from './components/StatCard';
import { useAuth } from './hooks/useAuth';
import { useDashboard } from './hooks/useDashboard';
import type { AuthUser } from './types/auth';

const emptyDashboard = {
  homes: 0,
  devices: { total: 0, online: 0, warning: 0 },
  consumption24h: { energyKwh: 0, waterLiters: 0, gasM3: 0 },
  recentDevices: [],
};

function DashboardApp({ user, onLogout }: { user: AuthUser; onLogout: () => void }) {
  const { data, error } = useDashboard();
  const dashboard = data ?? emptyDashboard;
  const connectedPercent = dashboard.devices.total
    ? Math.round((dashboard.devices.online / dashboard.devices.total) * 100)
    : 0;
  const displayName = user.first_name || user.username;

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <header className="topbar" id="inicio">
          <div className="topbar-copy">
            <p className="eyebrow">Dashboard</p>
            <h1>Hola, {displayName}</h1>
            <p className="subtitle">Resumen general de tu hogar inteligente.</p>
          </div>

          <div className="topbar-actions">
            <div className="user-summary" aria-label={`Sesión de ${displayName}`}>
              <div className="avatar" aria-hidden="true">{displayName.slice(0, 1).toUpperCase()}</div>
              <div>
                <strong>{displayName}</strong>
                <span>Administrador</span>
              </div>
            </div>
            <button className="logout-button" onClick={onLogout} title="Cerrar sesión" aria-label="Cerrar sesión">
              <FontAwesomeIcon icon={faRightFromBracket} />
              <span>Cerrar sesión</span>
            </button>
          </div>
        </header>

        {error && <div className="connection-warning">{error}</div>}

        <section className="hero-panel">
          <div className="hero-copy">
            <span className="hero-kicker"><FontAwesomeIcon icon={faLeaf} /> EcoHome Smart Living</span>
            <h2>Tecnología para un hogar <span>más consciente.</span></h2>
            <p>Controla tus dispositivos, monitorea recursos y automatiza tareas desde un mismo lugar.</p>
          </div>
          <div className="hero-status">
            <div className="hero-status-icon"><FontAwesomeIcon icon={faCircleCheck} /></div>
            <div>
              <strong>Todo en orden</strong>
              <span>{dashboard.devices.online} de {dashboard.devices.total} dispositivos en línea</span>
            </div>
          </div>
        </section>

        <section className="stats-grid" aria-label="Indicadores principales">
          <StatCard label="Hogares" value={String(dashboard.homes)} detail="registrados" icon={faHouse} accent="green" />
          <StatCard label="Dispositivos" value={`${dashboard.devices.online}/${dashboard.devices.total}`} detail={`${connectedPercent}% conectados`} icon={faMicrochip} accent="blue" />
          <StatCard label="Energía · 24 h" value={`${dashboard.consumption24h.energyKwh.toFixed(1)} kWh`} detail="consumo" icon={faBolt} accent="orange" />
          <StatCard label="Agua · 24 h" value={`${dashboard.consumption24h.waterLiters.toFixed(0)} L`} detail="consumo" icon={faDroplet} accent="cyan" />
        </section>

        <section className="content-grid dashboard-primary"><SimulatorPanel hasHome={dashboard.homes > 0} /></section>
        <section className="content-grid"><RecommendationsOverview /></section>
        <section className="content-grid"><AdvancedAnalytics /></section>
        <section className="content-grid"><SecurityOverview /><ResourceOverview /></section>

        <section className="content-grid" id="dispositivos">
          <article className="panel devices-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">IoT</p><h3>Dispositivos recientes</h3></div>
              <span className="device-count">{dashboard.recentDevices.length}</span>
            </div>
            {dashboard.recentDevices.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon"><FontAwesomeIcon icon={faMicrochip} /></div>
                <strong>Sin actividad reciente</strong>
                <p>Los dispositivos conectados aparecerán aquí.</p>
              </div>
            ) : dashboard.recentDevices.map((device) => (
              <div className="device-row" key={device.id}>
                <div className="device-icon"><FontAwesomeIcon icon={faMicrochip} /></div>
                <div className="device-copy">
                  <strong>{device.name}</strong>
                  <span>{device.room ?? 'Sin habitación'} · {device.type}</span>
                </div>
                <DeviceStatus status={device.status} />
              </div>
            ))}
          </article>
        </section>

        <section className="content-grid"><OperationsOverview /></section>
      </main>
    </div>
  );
}

export default function App() {
  const auth = useAuth();

  if (auth.loading) return <div className="auth-loading">Cargando EcoHome…</div>;
  if (!auth.user) return <LoginScreen error={auth.error} onLogin={auth.login} />;

  return <DashboardApp user={auth.user} onLogout={auth.logout} />;
}
