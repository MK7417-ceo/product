import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001', // M1 dev: live test backend
        changeOrigin: true,
      },
    },
  },
  build: {
    // Speed: pull React + its runtime deps out of the main entry chunk
    // into one stable vendor chunk. Route chunks are already split by
    // React.lazy in App.tsx; this only stops the 347 kB entry chunk from
    // changing hash (and re-downloading) on every app-code change, since
    // vendor-react only changes when React itself is upgraded.
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (
            id.includes('node_modules/react') ||
            id.includes('node_modules/scheduler')
          ) {
            return 'vendor-react';
          }
          return undefined;
        },
      },
    },
  },
})
