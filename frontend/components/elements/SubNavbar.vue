<template>
	<div>
		<div
      class="w-full flex sm:border-b sm:border-gray-300 relative flex-col sm:flex-row justify-items-center"
    >
      <div @click="isDashboard()"
        :class="dashboard ? 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 border-b-4 border-green-500' : 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 border-b-4'"
      >
        Dashboard
      </div>
      <div @click="isUpload()"
        :class="upload ? 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 border-b-4 border-green-500' : 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 border-b-4'"
      >
        Upload
      </div>
    </div>
	</div>
</template>
<script>
import { mapFields } from "vuex-map-fields";
export default {
    name: "default",
    data: () => ({
        upload: false,
        dashboard: true
    }),
    computed: {
      ...mapFields("base", ["metadataname"])
    },
    methods: {
        async isUpload() {
            await this.$router.push(`/create/upload?name=${this.$route.query.name}`)
            this.dashboard = false
            this.upload = true
            await this.$store.dispatch('base/MetadataList', {project_name: this.$route.query.name.split("_")[1]})
            await this.$store.dispatch('base/ProjectConfig', {name: this.$route.query.name.split("_")[1]})
            await this.$store.dispatch('base/MetadataConfig', {project: this.$route.query.name.split("_")[1], name: this.metadataname})
        },
        async isDashboard() {
            this.dashboard = true
            this.upload = false
            this.$store.dispatch('base/ProjectInfo', {name: this.$route.query.name})
            this.$router.push(`/?name=${this.$route.query.name}`)
        }
    },
};
</script>