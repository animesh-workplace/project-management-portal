import jwt_decode from 'jwt-decode'
import { getField, updateField } from 'vuex-map-fields'

export const state = () => ({
    theme: 'light',
    navbar_active: 'Upload',
})

export const getters = {
    getField,
}

export const mutations = {
    updateField,
    SET_THEME(state, payload) {
        state.theme = payload
    },
}

export const actions = {
    async nuxtServerInit({ commit, dispatch }, { app, store }) {
        const csrf_token = app.$cookies.get('XSRF-TOKEN')
        const access_token = app.$cookies.get('JWT-AUTH')
        const refresh_token = app.$cookies.get('JWT-REFRESH')
        if (access_token != undefined && refresh_token != undefined) {
            await store.dispatch('auth/GetAuthStatus', 'Authenticated')
        } else {
            await store.dispatch('auth/GetAuthStatus', 'Unauthenticated')
        }
        if (store.state.auth.authenticated) {
            const jwt_exp = jwt_decode(access_token).exp
            const diff_ms = app.$dayjs.unix(jwt_exp).diff(app.$dayjs())
            await store.dispatch('auth/SetTokenExpiration', diff_ms)
        }
    },
    SetTheme({ commit, dispatch }, payload) {
        if (payload == 'dark') {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
        localStorage.setItem('theme', payload)
    },
    GetTheme({ commit, dispatch, state }) {
        let theme = localStorage.getItem('theme')
        if (theme == null) {
            dispatch('SetTheme', state.theme)
        } else {
            commit('SET_THEME', theme)
            dispatch('SetTheme', theme)
        }
    },
}
