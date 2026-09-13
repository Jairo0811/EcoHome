import type { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

interface StatCardProps {
  label: string;
  value: string;
  detail: string;
  icon: IconDefinition;
  accent?: 'green' | 'blue' | 'cyan' | 'orange';
}

export function StatCard({ label, value, detail, icon, accent = 'blue' }: StatCardProps) {
  return (
    <article className={`stat-card accent-${accent}`}>
      <div className="stat-icon" aria-hidden="true">
        <FontAwesomeIcon icon={icon} />
      </div>
      <div className="stat-copy">
        <p className="eyebrow">{label}</p>
        <strong className="stat-value">{value}</strong>
        <p className="stat-detail">{detail}</p>
      </div>
    </article>
  );
}
