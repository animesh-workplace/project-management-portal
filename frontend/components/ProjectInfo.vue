<template>
	<div>
		<ElementsSubNavbar />
		<div class="flex items-center">
	    	<!-- <p v-if="keys.length==0" class="w-5/12 mx-auto md:mx-0 text-emerald-900 text-lg font-bold">
	            Project does not have the data!. Upload here...
	        </p> -->
		  <div class="max-w-7xl mx-auto">
	            <div class="flex flex-col">
	                <div class="overflow-x-auto shadow-md sm:rounded-lg">
	                    <div class="inline-block w-full align-middle">
	                        <table
	                            class="w-full divide-y divide-gray-200 table-fixed dark:divide-gray-700" v-if="keys.length>0"
	                        >
	                            <thead class="bg-green-400 dark:bg-gray-700">
	                                <tr class="bg-primary text-center">
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white uppercase dark:text-gray-400" v-for="event in keys"
	                                    >
	                                        {{ event }}
	                                    </th>
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white uppercase dark:text-gray-400"
	                                    >
	                                        Metadata
	                                    </th>
	                                </tr>
	                            </thead>
	                            <tbody
	                                class="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700"
	                            >
	                                <tr
	                                    class="hover:bg-gray-100 dark:hover:bg-gray-700 text-center" v-for="event in projectInfo" :key="event.id"
	                                >
	                                    <td
	                                        class="py-2 px-6 text-sm font-medium text-gray-900 whitespace-nowrap dark:text-white" v-for="value in event"
	                                    >
	                                        {{ value }}
	                                    </td>
	                                    <td
	                                        class="py-2 px-6 text-sm font-medium text-gray-900 whitespace-nowrap dark:text-white"
	                                    >
	                                        <a
		                                        @click="metaData(event)"
		                                        target="_blank"
		                                        class="text-blue-600 dark:text-blue-500 hover:underline cursor-pointer"
		                                        >View</a
		                                    >
	                                    </td>
	                                </tr>
	                            </tbody>
	                        </table>
	                    </div>
	                </div>
	            </div>
	        </div>
		</div>
	</div>
</template>

<script>
	import { mapFields } from "vuex-map-fields";
	export default {
	    data: () => ({
	        params: {
	        	name: ""
	        },
	        keys: []
	    }),
	    methods: {
	    	async metaData(value) {
	    		this.name = this.$route.query.name.split('_')[1]
	    		this.$router.push(`/metadatainfo?name=${this.$route.query.name}&module=${this.metadataname}&id=${value.id}&${Object.keys(value)}=${Object.values(value)}`)

	    		this.baseURL["module"] = this.metadataname
	    		this.baseURL["id"] = value.id
	    		this.baseURL[Object.keys(value)] = Object.values(value)

	    		this.$store.dispatch("base/MetadataList", {project_name: this.name})
	    		this.$store.dispatch("base/MetadataInfo", {name: `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.metadataname}_metadata`, m_id: value.id})
	    	}
	    },
	    watch: {
			projectInfo(value) {
				if (Object.keys(value).length > 0) {
					this.keys = Object.keys(value[0])
				} else {
					this.keys = []
				}
			},
		},
	    computed: {
	        ...mapFields("base", [
	        	"baseURL",
	        	"name",
	        	"metadataname",
	            "projectList",
	            "projectList_loded",
	            "projectInfo",
	            "projectInfo_loaded"
	        ]),
	    },
	    mounted() {
	    	this.$nextTick(() => {
	    		this.name = this.name
				this.params.name = `${this.$route.query.name}`
				this.$store.dispatch("base/ProjectList")
 	           	this.$store.dispatch("base/ProjectInfo", this.params)
			})
	    },
	};
</script>