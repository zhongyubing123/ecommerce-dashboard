import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {   // ⚠️ 这里必须是 server，不是 proxy 单独写
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
        
      }
    }
  }
})