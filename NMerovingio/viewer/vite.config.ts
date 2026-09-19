import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [path.resolve(here, '..')]
    }
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      input: {
        graph: path.resolve(here, 'index.html'),
        workspace: path.resolve(here, 'workspace.html')
      }
    }
  }
})
