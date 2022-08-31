<template>
	<div>
		<ElementsSubNavbar />
		<p v-if="$route.query.name" class="text-xl font-bold flex justify-center uppercase">{{$route.query.name.split("_",)[1]}} information</p>
		<div class="flex items-center">
	    	<div
		      v-show="isShowing"
		      class="fixed inset-10 w-2/3 h-4 mx-auto pt-24 py-16 mr-36 grid justify-center z-30"
		      id="my-modal"
		    >
		      <div v-show="isShowing" class="w-full shadow p-5 rounded-lg bg-gray-50">
		    	<p class="text-xl font-bold flex justify-center">Click on delete button to remove the record</p>
		        <div class="flex items-center mt-4">
					<div class="mx-auto grid gap-6 mb-6 lg:grid-cols-3 flex justify-center items-center">
				        <div v-for="event in keys.slice(1,).length">
				            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300 capitalize">{{keys[event].replaceAll("_"," ")}}</label>
				            <input type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-40 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 capitalize" :value="values[event]" readonly>
				        </div>
				    </div>
				</div>
				<div class="flex justify-center items-center">
				    <div class="mx-auto grid gap-6 mb-6 lg:grid-cols-2 w-80 flex justify-center items-center">
				        <button @click="cancelDelete()"
			                class="px-10 py-2 mt-8 font-semibold text-sm bg-red-400 hover:bg-red-500 text-white items-center rounded-full shadow-sm"
			            >
			                Cancel
			            </button>
			            <button @click="deleteSampleIdentifier()"
			                class="px-10 py-2 mt-8 font-semibold text-sm bg-blue-400 text-white rounded-full shadow-sm hover:bg-blue-500"
			            >
			                Delete
			            </button>
				    </div>
				</div>
		      </div>
		    </div>
		  <div class="max-w-7xl mx-auto">
	            <div class="flex flex-col">
	                <div class="overflow-x-auto shadow-md sm:rounded-lg">
	                    <div class="inline-block w-full align-middle">
	                        <table
	                            class="w-full divide-y divide-gray-200 table-fixed dark:divide-gray-700" v-if="keys.length>0"
	                        >
	                            <thead class="bg-green-400 dark:bg-gray-700">
	                                <tr class="bg-primary text-center capitalize">
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white dark:text-gray-400" v-for="event in keys"
	                                    >
	                                        {{ event.replaceAll("_", " ") }}
	                                    </th>
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white dark:text-gray-400"
	                                    >
	                                        Metadata
	                                    </th>
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white dark:text-gray-400"
	                                    >
	                                        Actions
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
	                                    <div>
                                            <button @click="updateSI(event)"
                                                class="px-3 py-0.5 mt-1 font-semibold text-sm bg-green-500 text-white rounded-full shadow-sm"
                                            >
                                                Edit
                                            </button>
                                            <button @click="veiwDeletePage(event)"
                                                class="px-1.5 py-1 mt-1 font-semibold text-xs bg-red-500 text-white rounded-full shadow-sm"
                                            >
                                                Delete
                                            </button>
                                        </div>
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
	        keys: [],
	        values: [],
	        isShowing: false
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
	    	},
	    	updateSI(value) {
	    		this.$router.push(`/update/sample_identifier?name=${this.$route.query.name}&module=${this.metadataname}&id=${value.id}&${Object.keys(value)}=${Object.values(value)}`)
	    	},
	    	veiwDeletePage(value) {
	    		this.values = Object.values(value)
	    		this.isShowing = true
			},
			cancelDelete() {
				this.isShowing = false
			},
			async deleteSampleIdentifier() {
				this.$store.dispatch("base/DeleteSampleIdentifier", {"name": this.$route.query.name, "pk": this.values[0]})
				this.isShowing = false
			},
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