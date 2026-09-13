import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { SecurityOverview } from './SecurityOverview';
import { useSecurity } from '../hooks/useSecurity';

vi.mock('../hooks/useSecurity', () => ({
  useSecurity: vi.fn(),
}));

const mockedUseSecurity = vi.mocked(useSecurity);
const setMode = vi.fn();

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

function renderMode(mode: 'DISARMED' | 'HOME' | 'AWAY') {
  mockedUseSecurity.mockReturnValue({
    states: [{ id: 1, home: 7, mode, updated_at: '2026-09-13T12:00:00Z' }],
    events: [],
    error: null,
    setMode,
  });

  render(<SecurityOverview />);
}

describe('SecurityOverview', () => {
  it.each([
    ['DISARMED', 'Desarmar', 'Desarmado'],
    ['HOME', 'En casa', 'En casa'],
    ['AWAY', 'Fuera', 'Fuera'],
  ] as const)('highlights the active %s mode', (mode, buttonName, label) => {
    renderMode(mode);

    const activeButton = screen.getByRole('button', { name: buttonName });
    expect(activeButton.getAttribute('aria-pressed')).toBe('true');
    expect(activeButton.className).toContain('primary-button');
    expect(screen.getByText(label, { selector: '.period-chip' })).toBeTruthy();
  });

  it('sends the selected security mode to the API hook', () => {
    renderMode('DISARMED');

    fireEvent.click(screen.getByRole('button', { name: 'Fuera' }));

    expect(setMode).toHaveBeenCalledWith(7, 'AWAY');
  });
});
