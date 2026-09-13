import { useEffect, useState } from 'react';

import { api } from '../api/http';

type Props = {
  hasHome: boolean;
};

const NO_HOME_MESSAGE = 'Necesitas un hogar configurado antes de ejecutar la simulación.';
const READY_MESSAGE = 'Listo para generar datos de prueba.';

export function SimulatorPanel({ hasHome }: Props) {
  const [status, setStatus] = useState(hasHome ? READY_MESSAGE : NO_HOME_MESSAGE);

  useEffect(() => {
    setStatus((current) => {
      if (!hasHome) return NO_HOME_MESSAGE;
      if (current === NO_HOME_MESSAGE) return READY_MESSAGE;
      return current;
    });
  }, [hasHome]);

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
