import { useState } from 'react';

import { api } from '../api/http';

type Props = {
  hasHome: boolean;
};

export function SimulatorPanel({ hasHome }: Props) {
  const [status, setStatus] = useState(
    hasHome
      ? 'Listo para generar datos de prueba.'
      : 'Necesitas un hogar configurado antes de ejecutar la simulación.',
  );

  async function run() {
    if (!hasHome) return;

    setStatus('Simulando…');
    try {
      const result = await api.runSimulation(10);
      setStatus(`${result.telemetryCreated} lecturas sintéticas generadas en el hogar #${result.home}.`);
    } catch (cause) {
      setStatus(cause instanceof Error ? cause.message : 'La simulación falló.');
    }
  }

  return (
    <article className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Laboratorio IoT</p>
          <h3>Simulador de telemetría</h3>
        </div>
        <button className="primary-button" type="button" disabled={!hasHome} onClick={() => void run()}>
          Simular 10 ciclos
        </button>
      </div>
      <p className="subtitle">{status}</p>
    </article>
  );
}
