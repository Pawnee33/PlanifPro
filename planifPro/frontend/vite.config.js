import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',     // le service worker se met à jour tout seul
      devOptions: { enabled: true },  // permet de tester la PWA en mode dev
      manifest: {
        name: 'PlanifPro',
        short_name: 'PlanifPro',
        description: 'Gestion de planning pédagogique entre professeurs et élèves',
        theme_color: '#0C2863',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: 'pwa-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
})
