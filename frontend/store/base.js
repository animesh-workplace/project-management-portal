import { getField, updateField } from "vuex-map-fields";

export const state = () => ({
	baseURL: {},
	projectList: {},
	projectList_loaded: false,

	name: "",
	metadataname: "",
	projectInfo: {},
	projectInfo_loaded: false,

	metadataList: {},
	metadataInfo: {},

	projectConfig: {},
	metadataConfig: [],

	projectDataToUpload: [],
	projectDataToUpdate: []

});

export const getters = {
	getField,
};

export const mutations = {
	SET_ProjectList(state, payload) {
		state.projectList = payload;
		state.projectList_loaded = true;
		state.name = state.projectList.projects[0]
	},
	SET_ProjectInfo(state, payload) {
		state.projectInfo = payload;
		state.projectInfo_loaded = true;
	},
	SET_MetadataList(state, payload) {
		state.metadataList = payload;
		state.metadataname = state.metadataList.metadata[0]
	},
	SET_MetadataInfo(state, payload) {
		state.metadataInfo = payload;
	},
	SET_ProjectConfig(state, payload) {
		state.projectConfig = payload
	},
	SET_MetadataConfig(state, payload) {
		state.metadataConfig = payload
	},

	SET_ProjectToUpload(state, payload) {
		state.projectDataToUpload = payload
	},
	SET_ProjectToUpdate(state, payload) {
		state.projectDataToUpdate = payload
	},
	updateField,
};

export const actions = {
	async ProjectList({ commit, dispatch }) {
		const response = await this.$axios.$post(
			'http://10.10.6.87/pmp/api/schema/projects/names/'
		);
		await commit("SET_ProjectList", response);
	},
	async ProjectInfo({ commit, dispatch }, payload) {
		await dispatch("ProjectList");
		const response = await this.$axios.$post(
			'http://10.10.6.87/pmp/api/schema/projects/info/', payload
		);
		await commit("SET_ProjectInfo", response);
	},
	async MetadataList({ commit, dispatch }, payload) {
		const response = await this.$axios.$post(
			'http://10.10.6.87/pmp/api/schema/metadata/names/', payload
		);
		await commit("SET_MetadataList", response);
	},
	async MetadataInfo({ commit, dispatch, state }, payload) {
		try {
			// await dispatch("MetadataList", {project_name: state.name});
			const response = await this.$axios.$post(
				'http://10.10.6.87/pmp/api/schema/metadata/info/', payload
			);
			await commit("SET_MetadataInfo", response);
		} catch (err) {
			// state.projectInfo = {}
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async CreateSampleIdentifier({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/create/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async CreateMetadata({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/metadata/create/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async ProjectConfig({ commit, dispatch }, payload) {
		const response = await this.$axios.$post(
			'http://10.10.6.87/pmp/api/schema/projects/config/', payload
		);
		await commit("SET_ProjectConfig", response);
	},
	async MetadataConfig({ commit, dispatch }, payload) {
		const response = await this.$axios.$post(
			'http://10.10.6.87/pmp/api/schema/metadata/config/', payload
		);
		await commit("SET_MetadataConfig", response);
	},
	async SeperateProjectData({ commit, dispatch }, payload) {
		try {
	        const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/seperate/', payload)
	        await commit("SET_ProjectToUpload", response.dataToUpload);
	        await commit("SET_ProjectToUpdate", response.dataToUpdate);
		} catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async BulkUpdateProject({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/bulk-update/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async UploadProject({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/upload/', payload
			)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async UploadMetadata({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/metadata/upload/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async UpdateProject({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/update/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async UpdateMetadata({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/metadata/update/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async DeleteSampleIdentifier({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/projects/delete/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
	async DeleteMetadata({ commit, dispatch }, payload) {
		try {
            const response = await this.$axios.$post('http://10.10.6.87/pmp/api/schema/metadata/delete/', payload)
            this.$notification.show(response.code, response.message, 'SUCCESS')
        } catch (err) {
            this.$notification.show(err.response.statusText, Object.values(err.response.data)[0], 'ERROR')
        }
	},
};
