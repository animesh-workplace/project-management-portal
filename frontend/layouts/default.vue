<template>
    <div class="bg-gray-100">
        <NavBar/>
        <div class="grid grid-flow-col col-span-13">
            <div class="flex justify-right">
                <SideNavBar/>
            </div>
            <div class="col-span-12 pt-2 ml-4 mr-4">
                <Nuxt />
            </div>
        </div>
    </div>
</template>
<script>
import { mapFields } from "vuex-map-fields";
export default {
    name: "default",
    data: () => ({
    }),
    async created() {
        if (this.username) {
            await this.$store.dispatch("base/ProjectList", {name: this.username});
            await this.$router.push(`/?name=${this.username}_${this.name}_si`)
            await this.$store.dispatch("base/ProjectInfo", {name: `${this.username}_${this.name}_si`})
            await this.$store.dispatch("base/MetadataList", {project_name: this.$route.query.name.split("_")[1]})
        }
    },
    computed: {
        ...mapFields("base", ["name"]),
        ...mapFields("auth", ["username"]),
    },
    async mounted() {
        await this.$nextTick(() => {
            if (this.$route.query.name) {
                this.$store.dispatch("base/MetadataList", {project_name: this.$route.query.name.split("_")[1]})
                this.$store.dispatch("base/ProjectInfo", {name: this.$route.query.name})
            }
        })
    },
};
</script>