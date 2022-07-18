export default ({ app }, inject) => {
	const notification = {
		show(title, message, mode, timeout = 10) {
			if (mode == 'SUCCESS') {
				app.$toast.show({
					timeout: timeout,
					title: title,
					type: 'success',
					message: message,
					classTitle: 'text-white',
					classClose: 'text-white',
					classMessage: 'text-white',
					classToast: 'bg-emerald-600',
				})
			} else if (mode == 'ERROR') {
				app.$toast.show({
					timeout: timeout,
					title: title,
					type: 'danger',
					message: message,
					classTitle: 'text-white',
					classClose: 'text-white',
					classToast: 'bg-rose-600',
					classMessage: 'text-white',
				})
			} else if (mode == 'WARNING') {
				app.$toast.show({
					timeout: timeout,
					title: title,
					type: 'warning',
					message: message,
					classTitle: 'text-white',
					classClose: 'text-white',
					classMessage: 'text-white',
					classToast: 'bg-amber-500',
				})
			}
		},
	}
	inject('notification', notification)
}
