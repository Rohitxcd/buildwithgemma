import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/protect': 'http://127.0.0.1:8000',
      '/upload': 'http://127.0.0.1:8000',
      '/report': 'http://127.0.0.1:8000',
      '/uploads': 'http://127.0.0.1:8000',
      '/protected': 'http://127.0.0.1:8000',
    }
  }
});
