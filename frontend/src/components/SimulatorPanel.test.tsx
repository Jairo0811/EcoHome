import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { SimulatorPanel } from './SimulatorPanel';

afterEach(cleanup);

describe('SimulatorPanel', () => {
  it('disables simulation when the user has no configured home', () => {
    render(<SimulatorPanel hasHome={false} />);

    expect(screen.getByRole('button', { name: 'Simular 10 ciclos' })).toBeDisabled();
    expect(screen.getByText('Necesitas un hogar configurado antes de ejecutar la simulación.')).toBeTruthy();
  });
});
