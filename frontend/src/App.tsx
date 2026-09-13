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

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <header className="topbar" id="inicio">
          <div>
            <p className="eyebrow">Panel general</p>
            <h1>Hola, {user.first_name || user.username} 👋</h1>
            <p className="subtitle">Plataforma integral de hogar inteligente.</p>
          </div>
          <button className="logout-button" onClick={onLogout}>Cerrar sesión</button>
        </header>

        {error && <div className="connection-warning">{error}</div>}

        <section className="hero-panel">
          <div className="hero-copy">
            <span className="hero-kicker">EcoHome Smart Living</span>
            <h2>Observa, automatiza, simula y optimiza.</h2>
          </div>
        </section>

        <section className="stats-grid">
          <StatCard label="Hogares" value={String(dashboard.homes)} detail="registrados" icon="⌂" accent="green" />
          <StatCard label="Dispositivos" value={`${dashboard.devices.online}/${dashboard.devices.total}`} detail={`${connectedPercent}% conectados`} icon="◉" accent="blue" />
          <StatCard label="Energía · 24 h" value={`${dashboard.consumption24h.energyKwh.toFixed(1)} kWh`} detail="consumo" icon="⚡" accent="cyan" />
          <StatCard label="Agua · 24 h" value={`${dashboard.consumption24h.waterLiters.toFixed(0)} L`} detail="consumo" icon="◌" accent="blue" />
        </section>

        <section className="content-grid"><SimulatorPanel /></section>
        <section className="content-grid"><RecommendationsOverview /></section>
        <section className="content-grid"><AdvancedAnalytics /></section>
        <section className="content-grid"><SecurityOverview /><ResourceOverview /></section>

        <section className="content-grid" id="dispositivos">
          <article className="panel devices-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">IoT</p><h3>Dispositivos recientes</h3></div>
            </div>
            {dashboard.recentDevices.map((device) => (
              <div className="device-row" key={device.id}>
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
