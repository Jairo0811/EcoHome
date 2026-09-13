import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { Sidebar } from './Sidebar';

afterEach(cleanup);

describe('Sidebar', () => {
  it('scrolls to a real dashboard section when a navigation item is selected', () => {
    const section = document.createElement('section');
    section.id = 'dispositivos';
    section.scrollIntoView = vi.fn();
    document.body.appendChild(section);

    render(<Sidebar />);
    fireEvent.click(screen.getByRole('button', { name: 'Dispositivos' }));

    expect(section.scrollIntoView).toHaveBeenCalledWith({ behavior: 'smooth', block: 'start' });
    expect(screen.getByRole('button', { name: 'Dispositivos' }).getAttribute('aria-current')).toBe('page');
  });

  it('does not expose navigation entries without implemented destinations', () => {
    render(<Sidebar />);

    expect(screen.queryByText('Mi hogar')).toBeNull();
    expect(screen.queryByText('Habitaciones')).toBeNull();
    expect(screen.getByText('EcoHome 1.1.0')).toBeTruthy();
  });
});
