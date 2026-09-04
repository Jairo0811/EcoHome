import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { DeviceStatus } from './DeviceStatus';

describe('DeviceStatus', () => {
  it.each([
    ['ONLINE', 'En línea'],
    ['OFFLINE', 'Fuera de línea'],
    ['WARNING', 'Advertencia'],
  ] as const)('muestra %s como "%s"', (status, label) => {
    render(<DeviceStatus status={status} />);

    expect(screen.getByText(label)).toBeTruthy();
  });
});
