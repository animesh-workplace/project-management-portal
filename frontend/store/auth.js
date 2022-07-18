import { getField, updateField } from 'vuex-map-fields'

export const state = () => ({
    profile: {},
    username: '',
    refresh_token: false,
    authenticated: false,
    token_expiration: false,
})

export const getters = {
    getField,
}

export const mutations = {
    RESET(state) {
        state.profile = {}
        state.username = ''
        state.authenticated = false
    },
    SET_USERNAME(state, payload) {
        state.username = payload
    },
    SET_PROFILE(state, payload) {
        state.profile = payload
    },
    SET_AUTHENTICATION(state, payload) {
        state.authenticated = payload
    },
    SET_REFRESH_TOKEN(state, payload) {
        state.refresh_token = payload
    },
    SET_TOKEN_EXPIRATION(state, payload) {
        state.token_expiration = payload
    },
    SET_AUTH_STATUS(state, payload) {
        if (payload == 'Authenticated') {
            state.authenticated = true
        } else if (payload == 'Unauthenticated') {
            state.authenticated = false
        }
    },
    updateField,
}

export const actions = {
    async StartLogin({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.$post('/auth/login/', payload, {
                withCredentials: true,
                credentials: 'include',
            })
            await dispatch('SetTokenExpiration', this.$dayjs(response.expiration).diff(this.$dayjs()))
            await dispatch('GetUser')
            await commit('SET_AUTHENTICATION', true)
            this.$router.push('/upload')
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
    },
    async StartRegistration({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.$post('/auth/register/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
    },
    async StartActivation({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.$post('/auth/activate/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
            this.$router.push('/')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
    },
    async GetUser({ commit }) {
        try {
            const response = await this.$axios.$post('/auth/user/')
            await commit('SET_USERNAME', response.data.username)
            await commit('SET_PROFILE', response.data)
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
    },
    async StartLogout({ commit }) {
        try {
            const response = await this.$axios.$post('/auth/logout/')
            await commit('RESET')
            this.$router.push('/')
            this.$notification.show('Logout', response.message, 'WARNING')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
    },
    async SetTokenExpiration({ commit, dispatch }, payload) {
        await commit('SET_TOKEN_EXPIRATION', payload)
    },
    // CreateTimer cannot have async property, otherwise the timer won't work
    CreateTimer({ commit, dispatch }, payload) {
        if (payload < 60000) {
            dispatch('StartLogout')
        } else {
            setTimeout(() => {
                dispatch('StartLogout')
            }, payload - 60000)
        }
    },
    // GetAuthStatus works during server side rendering
    // It cannot have this.$notification.show() as it works on client side
    async GetAuthStatus({ commit, dispatch }, payload) {
        await commit('SET_AUTH_STATUS', payload)
        // try {
        //     const response = await this.$axios.$post('/auth/verify/')
        //     if (response.message == 'Refreshable') {
        //         if (process.server) {
        //             await commit('SET_REFRESH_TOKEN', true)
        //             await commit('SET_AUTHENTICATION', true)
        //         } else {
        //             await dispatch('RefreshToken')
        //         }
        //     } else {
        //         await commit('SET_AUTH_STATUS', response.message)
        //     }
        // } catch (err) {
        //     console.log(err)
        // }
    },
    // RefreshToken works during server side rendering
    // It cannot have this.$notification.show() as it works on client side
    async RefreshToken({ commit, dispatch }) {
        try {
            const response = await this.$axios.$post(
                '/auth/refresh/',
                {},
                {
                    withCredentials: true,
                    credentials: 'include',
                },
            )
            await dispatch('SetTokenExpiration', this.$dayjs(response.expiration).diff(this.$dayjs()))
            await commit('SET_AUTHENTICATION', true)
            await commit('SET_REFRESH_TOKEN', false)
        } catch (err) {
            await commit('SET_AUTHENTICATION', false)
            await commit('SET_REFRESH_TOKEN', false)
            console.log(err)
        }
    },
}
