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
      <section className="auth-card">
        <div className="auth-mark">⌂</div>
        <p className="eyebrow">EcoHome</p>
        <h1>Control inteligente para tu hogar</h1>
        <p className="subtitle">Inicia sesión para administrar hogares, dispositivos y consumo.</p>
        <form onSubmit={submit} className="auth-form">
          <label>Usuario<input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" required /></label>
          <label>Contraseña<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" required /></label>
          {error && <div className="auth-error">{error}</div>}
          <button className="primary-button" type="submit" disabled={submitting}>{submitting ? 'Ingresando…' : 'Iniciar sesión'}</button>
        </form>
      </section>
    </main>
  );
}
