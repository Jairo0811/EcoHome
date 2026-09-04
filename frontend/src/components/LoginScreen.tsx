import { FormEvent, useState } from 'react';

type Props = {
  error: string | null;
  onLogin: (username: string, password: string) => Promise<void>;
};

export function LoginScreen({ error, onLogin }: Props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    try {
      await onLogin(username, password);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-card" aria-labelledby="login-title">
        <div className="auth-mark" aria-hidden="true">⌂</div>
        <p className="eyebrow">EcoHome</p>
        <h1 id="login-title">Control inteligente para tu hogar</h1>
        <p className="subtitle">Inicia sesión para administrar hogares, dispositivos y consumo.</p>
        <form onSubmit={submit} className="auth-form" aria-busy={submitting}>
          <label>
            Usuario
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
              required
            />
          </label>
          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              required
            />
          </label>
          {error && <div className="auth-error" role="alert">{error}</div>}
          <button className="primary-button" type="submit" disabled={submitting}>
            {submitting ? 'Ingresando…' : 'Iniciar sesión'}
          </button>
        </form>
      </section>
    </main>
  );
}
