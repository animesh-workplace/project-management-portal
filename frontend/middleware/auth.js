export default async ({ app, $axios, store, redirect }) => {
    if (!store.state.auth.authenticated) {
        return redirect('/')
    }
}
