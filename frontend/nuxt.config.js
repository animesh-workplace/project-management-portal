export default {
  head: {
    title: 'frontend',
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
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    "@nuxtjs/auth-next",
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
    baseURL: "http://10.10.6.87/pmp/api/user",
  },

  auth: {
    strategies: {
      local: {
        scheme: "refresh",
        localStorage: {
          prefix: "auth.",
        },
        token: {
          prefix: "access_token.",
          property: "access_token",
          maxAge: 86400,
          type: "Bearer",
        },
        refreshToken: {
          prefix: "refresh_token.",
          property: "refresh_token",
          data: "refresh_token",
          maxAge: 60 * 60 * 24 * 15,
        },
        user: {
          property: "user",
          autoFetch: true,
        },
        endpoints: {
          login: { url: "/login/", method: "post" },
          refresh: { url: "/token/refresh/", method: "post" },
          user: { url: "/user", method: "get" },
          logout: { url: "/logout_view", method: "post" },
        },
        redirect: {
          login: "/login/",
          logout: "/login/",
          index: "/login/",
        },
      },
    },
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
