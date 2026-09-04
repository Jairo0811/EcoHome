import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import { LoginScreen } from './LoginScreen';

describe('LoginScreen', () => {
  it('envía las credenciales introducidas por el usuario', async () => {
    const user = userEvent.setup();
    const onLogin = vi.fn().mockResolvedValue(undefined);

    render(<LoginScreen error={null} onLogin={onLogin} />);

    await user.type(screen.getByLabelText('Usuario'), 'jairo');
    await user.type(screen.getByLabelText('Contraseña'), 'secreto');
    await user.click(screen.getByRole('button', { name: 'Iniciar sesión' }));

    await waitFor(() => {
      expect(onLogin).toHaveBeenCalledWith('jairo', 'secreto');
    });
  });

  it('muestra el error de autenticación recibido', () => {
    render(<LoginScreen error="Credenciales inválidas" onLogin={vi.fn()} />);

    expect(screen.getByText('Credenciales inválidas')).toBeTruthy();
  });

  it('marca usuario y contraseña como campos obligatorios', () => {
    render(<LoginScreen error={null} onLogin={vi.fn()} />);

    const username = screen.getByLabelText('Usuario') as HTMLInputElement;
    const password = screen.getByLabelText('Contraseña') as HTMLInputElement;

    expect(username.required).toBe(true);
    expect(password.required).toBe(true);
  });
});
