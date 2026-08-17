import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import App from './App';
import './index.css';
import './auth.css';
import './v1.css';

const root = document.getElementById('root');

if (!root) {
  throw new Error('No se encontró el contenedor raíz de EcoHome.');
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
