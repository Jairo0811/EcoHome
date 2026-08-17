import { DeviceStatus } from './components/DeviceStatus';
import { LoginScreen } from './components/LoginScreen';
import { ResourceOverview } from './components/ResourceOverview';
import { Sidebar } from './components/Sidebar';
import { StatCard } from './components/StatCard';
import { useAuth } from './hooks/useAuth';
import { useDashboard } from './hooks/useDashboard';
import type { AuthUser } from './types/auth';

const zeroSummary = { homes: 0, devices: { total: 0, online: 0, warning: 0 }, consumption24h: { energyKwh: 0, waterLiters: 0, gasM3: 0 }, recentDevices: [] };
const formatNumber = (value: number, maximumFractionDigits = 1) => new Intl.NumberFormat('es-DO', { maximumFractionDigits }).format(value);

function DashboardApp({ user, onLogout }: { user: AuthUser; onLogout: () => void }) {
  const { data, loading, error } = useDashboard();
  const dashboard = data ?? zeroSummary;
  const onlinePercentage = dashboard.devices.total > 0 ? Math.round((dashboard.devices.online / dashboard.devices.total) * 100) : 0;
  const displayName = user.first_name || user.username;

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <header className="topbar">
          <div><p className="eyebrow">Panel general</p><h1>Hola, {displayName} 👋</h1><p className="subtitle">Supervisa el estado, consumo y conectividad de tu hogar.</p></div>
          <div className="topbar-actions">
            <div className={`api-chip ${error ? 'api-offline' : ''}`}><span className="status-dot" />{loading ? 'Conectando…' : error ? 'API sin conexión' : 'Sistema operativo'}</div>
            <button className="logout-button" type="button" onClick={onLogout}>Cerrar sesión</button>
          </div>
        </header>
        {error && <div className="connection-warning" role="status"><strong>Backend no disponible.</strong><span>{error}</span></div>}
        <section className="hero-panel"><div className="hero-copy"><span className="hero-kicker">EcoHome Smart Living</span><h2>Tu hogar, más inteligente y eficiente.</h2><p>Centraliza consumo, dispositivos y automatización en una experiencia diseñada para reducir desperdicios y darte más control.</p><div className="hero-actions"><button className="primary-button" type="button">Explorar dispositivos</button><button className="secondary-button" type="button">Ver consumo</button></div></div><div className="home-orbit" aria-hidden="true"><div className="orbit-ring orbit-one"/><div className="orbit-ring orbit-two"/><div className="home-glyph">⌂</div><span className="orbit-node node-one">⚡</span><span className="orbit-node node-two">◉</span><span className="orbit-node node-three">♻</span></div></section>
        <section className="stats-grid" aria-label="Resumen de EcoHome">
          <StatCard label="Hogares" value={String(dashboard.homes)} detail="registrados en tu cuenta" icon="⌂" accent="green"/>
          <StatCard label="Dispositivos" value={`${dashboard.devices.online}/${dashboard.devices.total}`} detail={`${onlinePercentage}% conectados`} icon="◉" accent="blue"/>
          <StatCard label="Energía · 24 h" value={`${formatNumber(dashboard.consumption24h.energyKwh)} kWh`} detail="consumo acumulado" icon="⚡" accent="cyan"/>
          <StatCard label="Agua · 24 h" value={`${formatNumber(dashboard.consumption24h.waterLiters,0)} L`} detail="consumo acumulado" icon="◌" accent="blue"/>
        </section>
        <section className="content-grid"><ResourceOverview /></section>
        <section className="content-grid">
          <article className="panel consumption-panel"><div className="panel-heading"><div><p className="eyebrow">Recursos</p><h3>Consumo de las últimas 24 horas</h3></div><span className="period-chip">Tiempo real</span></div><div className="resource-list">
            <div className="resource-row"><div className="resource-label"><span className="resource-symbol energy">⚡</span><span>Energía</span></div><strong>{formatNumber(dashboard.consumption24h.energyKwh)} kWh</strong></div><div className="resource-bar"><span style={{width:`${Math.min(dashboard.consumption24h.energyKwh*3,100)}%`}}/></div>
            <div className="resource-row"><div className="resource-label"><span className="resource-symbol water">◌</span><span>Agua</span></div><strong>{formatNumber(dashboard.consumption24h.waterLiters,0)} L</strong></div><div className="resource-bar"><span style={{width:`${Math.min(dashboard.consumption24h.waterLiters/5,100)}%`}}/></div>
            <div className="resource-row"><div className="resource-label"><span className="resource-symbol gas">◈</span><span>Gas</span></div><strong>{formatNumber(dashboard.consumption24h.gasM3)} m³</strong></div><div className="resource-bar"><span style={{width:`${Math.min(dashboard.consumption24h.gasM3*8,100)}%`}}/></div>
          </div></article>
          <article className="panel devices-panel"><div className="panel-heading"><div><p className="eyebrow">IoT</p><h3>Dispositivos recientes</h3></div><span className="device-count">{dashboard.devices.total}</span></div>{dashboard.recentDevices.length===0?<div className="empty-state"><div className="empty-icon">◉</div><strong>Aún no hay dispositivos</strong><p>Los dispositivos vinculados aparecerán aquí.</p></div>:<div className="device-list">{dashboard.recentDevices.map(device=><div className="device-row" key={device.id}><div className="device-icon">◉</div><div className="device-copy"><strong>{device.name}</strong><span>{device.room??'Sin habitación'} · {device.type}</span></div><DeviceStatus status={device.status}/></div>)}</div>}</article>
        </section>
      </main>
    </div>
  );
}

export default function App() {
  const auth = useAuth();
  if (auth.loading) return <div className="auth-loading">Cargando EcoHome…</div>;
  if (!auth.user) return <LoginScreen error={auth.error} onLogin={auth.login}/>;
  return <DashboardApp user={auth.user} onLogout={auth.logout}/>;
}
