interface StatCardProps {
  label: string;
  value: string;
  detail: string;
  icon: string;
  accent?: 'green' | 'blue' | 'cyan';
}

export function StatCard({ label, value, detail, icon, accent = 'blue' }: StatCardProps) {
  return (
    <article className={`stat-card accent-${accent}`}>
      <div className="stat-icon" aria-hidden="true">{icon}</div>
      <div>
        <p className="eyebrow">{label}</p>
        <strong className="stat-value">{value}</strong>
        <p className="stat-detail">{detail}</p>
      </div>
    </article>
  );
}
