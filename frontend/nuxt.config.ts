// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss', 
    '@pinia/nuxt', 
    '@nuxtjs/color-mode',
    '@vercel/speed-insights/nuxt'
  ],
  colorMode: {
    classSuffix: '',
    preference: 'dark', // Default to dark mode
    fallback: 'dark'
  },
  runtimeConfig: {
    public: {
      // --- OPTION 1: LOCAL DEVELOPMENT (Default) ---
      // Uncomment this line for local development
      // apiBaseUrl: 'http://127.0.0.1:8000/api/'

      // --- OPTION 2: PRODUCTION (Render.com) ---
      // Uncomment this line when deploying to Vercel
      apiBaseUrl: 'https://cinesmart-api.onrender.com/api/'
    }
  }
})