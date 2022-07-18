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
    '@nuxtjs/axios', 'cookie-universal-nuxt', ['nuxt-tailvue', { toast: true }], '@nuxtjs/dayjs'
  ],
  axios: {},
  build: {
  }
}
