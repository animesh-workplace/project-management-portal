import { mapFields } from 'vuex-map-fields'

export default {
    computed: {
        ...mapFields('auth', ['authenticated', 'refresh_token', 'token_expiration']),
    },
    async fetch() {
        this.$store.dispatch('GetTheme')
        // if (this.refresh_token) {
        //     await this.$store.dispatch('auth/RefreshToken')
        // }
        if (this.authenticated) {
            await this.$store.dispatch('auth/GetUser')
            this.$store.dispatch('auth/CreateTimer', this.token_expiration)
        }
    },
    fetchOnServer: false,
    beforeMount() {},
}
