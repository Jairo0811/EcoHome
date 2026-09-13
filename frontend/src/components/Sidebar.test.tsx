import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { Sidebar } from './Sidebar';

afterEach(cleanup);

describe('Sidebar', () => {
  it('navega a una sección implementada y actualiza el estado activo', async () => {
    const destination = document.createElement('div');
    destination.id = 'consumo';
    destination.scrollIntoView = vi.fn();
    document.body.appendChild(destination);

    render(<Sidebar />);
    const button = screen.getByRole('button', { name: 'Consumo' });

    await userEvent.click(button);

    expect(destination.scrollIntoView).toHaveBeenCalledWith({ behavior: 'smooth', block: 'start' });
    expect(button.getAttribute('aria-current')).toBe('page');
  });

  it('no muestra destinos sin una vista implementada', () => {
    render(<Sidebar />);

    expect(screen.queryByRole('button', { name: 'Mi hogar' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Habitaciones' })).toBeNull();
  });
});
