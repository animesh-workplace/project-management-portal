<template>
    <div class="bg-gray-100">
        <NavBar/>
        <div class="grid grid-flow-col col-span-13">
            <div class="flex justify-right">
                <SideNavBar/>
            </div>
            <div class="col-span-12 pt-4 pr-2">
                <!-- <ElementsSubNavbar /> -->
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
    created() {
        if (this.username) {
            this.$store.dispatch("auth/GetUser");
            this.$store.dispatch("base/ProjectList");
            this.$store.dispatch("base/ProjectInfo", {name: `${this.username}_${this.name}_si`})
            this.$router.push(`/?name=${this.username}_${this.name}_si`)
        }
    },
    computed: {
        ...mapFields("base", ["name"]),
        ...mapFields("auth", ["username"]),
    },
    mounted() {
        this.$nextTick(() => {
            this.$store.dispatch("auth/GetUser")
            this.$store.dispatch("base/ProjectList")
            if (this.username) {
                this.$store.dispatch("base/MetadataList", {project_name: this.$route.query.name.split("_")[1]})
                this.$store.dispatch("base/ProjectInfo", {name: this.$route.query.name})
            }
        })
    },
};
</script>