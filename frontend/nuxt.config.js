export default {
  head: {
    title: 'pmp',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  css: [
  ],
  plugins: [
      '@/plugins/simple-vue-validator', { src: '@/plugins/notification', ssr: false },
  ],
  components: true,
  buildModules: [
    '@nuxtjs/tailwindcss','@nuxtjs/svg'
  ],
  modules: [
    'cookie-universal-nuxt', ['nuxt-tailvue', { toast: true }],
    '@nuxtjs/dayjs',
    '@nuxtjs/axios',
    // "@nuxtjs/auth-next",
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
    baseURL: "http://10.10.6.87/pmp/api/user",
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },
  server: {
    port: 3002,
  },
  router: {
    base: "/pmp/",
  },
}
