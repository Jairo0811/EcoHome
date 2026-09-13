import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { SimulatorPanel } from './SimulatorPanel';

afterEach(cleanup);

describe('SimulatorPanel', () => {
  it('disables simulation when the user has no configured home', () => {
    render(<SimulatorPanel hasHome={false} />);

    const button = screen.getByRole('button', { name: 'Simular 10 ciclos' });
    expect((button as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText('Necesitas un hogar configurado antes de ejecutar la simulación.')).toBeTruthy();
  });

  it('becomes ready when a home appears after the initial render', async () => {
    const { rerender } = render(<SimulatorPanel hasHome={false} />);

    rerender(<SimulatorPanel hasHome />);

    const button = screen.getByRole('button', { name: 'Simular 10 ciclos' });
    expect((button as HTMLButtonElement).disabled).toBe(false);
    expect(await screen.findByText('Listo para generar datos de prueba.')).toBeTruthy();
  });
});
