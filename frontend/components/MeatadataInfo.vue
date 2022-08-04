<template>
	<div>
		<ElementsSubNavbar />
		<div v-if="queryParams"
			class="mx-auto grid grid-cols-7 divide-x-2 divide-slate-400 p-2 mb-2 text-center divide-dashed text-sm flex justify-center items-center"
		>
			<div class="p-4 text-gray-400 bg-white rounded-l-md drop-shadow-md">
				<h2 class="text-base font-medium">{{queryKeys[0]}}</h2>
				<p>
					{{queryValues[0]}}
				</p> 
			</div>
			<div v-for="values in (queryValues.length-1)" class="p-4 text-gray-400 bg-white rounded-l-md drop-shadow-md">
				<h2 class="text-base font-medium">{{queryKeys[values]}}</h2>
				<p>
					{{queryValues[values]}}
				</p>
			</div>
		</div>
		<div
		  class="w-full flex sm:border-b sm:border-gray-300 relative flex-col sm:flex-row"
		>
		  <div v-for="event in metadataList.metadata" :key="event.id" @click="metaData(event)"
		    :class="$route.query.module != event ? 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-700 border-t-4 border-green-500 uppercase' : 'flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-700 border-b-4 text-green-700 bg-green-200 border-green-500 border-t-4 border-green-500 uppercase'"
		  >
		    {{ event }}
		  </div>
		</div>
		<div class="flex items-center mt-4">
			<div class="mx-auto grid gap-6 mb-6 lg:grid-cols-4 flex justify-center items-center">
		        <div v-for="event in keys.slice(1,)">
		            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300 capitalize">{{event.replaceAll("_"," ")}}</label>
		            <input type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 capitalize" :value="metadataInfo[event]" readonly>
		        </div>
		    </div>
		</div>
		<div class="flex items-center">
		  <div class="max-w-7xl mx-auto">
	            <div class="flex flex-col">
	                <div class="overflow-x-auto shadow-md sm:rounded-lg">
	                    <div class="inline-block w-full align-middle">
	                    	<h1 v-if="keys.length==0">Metadata is empty</h1>
	                        <table
	                            class="w-full divide-y divide-gray-200 dark:divide-gray-700" v-if="keys.length>0"
	                        >
	                            <thead class="bg-green-400 dark:bg-gray-700">
	                                <tr class="bg-primary text-center">
	                                    <th
	                                        class="py-3 px-6 text-lg font-medium tracking-wider text-white capitalize dark:text-gray-400" v-for="event in keys"
	                                    >
	                                        {{ event.replaceAll("_"," ") }}
	                                    </th>
	                                </tr>
	                            </thead>
	                            <tbody
	                                class="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700"
	                            >
	                                <tr
	                                    class="hover:bg-gray-100 dark:hover:bg-gray-700 text-center"
	                                >
	                                    <td
	                                        class="py-2 px-6 text-sm font-medium text-gray-900 whitespace-nowrap dark:text-white" v-for="event in metadataInfo" :key="event.id"
	                                    >
	                                        {{ event }}
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
	    	queryParams: "",
	    	queryKeys: [],
	    	queryValues: [],
	    	params: {
	    		name: "",
	    		m_id: 1
	    	},
	    	keys: []
	    }),
	    methods: {
	    	async metaData(value) {
	    		console.log(this.baseURL)
	    		this.params.name = `${this.username}_${this.$route.query.name.split('_')[1]}_${value}_metadata`
	    		this.params.m_id = this.$route.query.id
	    		this.$store.dispatch("base/MetadataInfo", this.params)
	    		this.$router.push(`/metadatainfo?name=${this.$route.query.name}&module=${value}&id=${this.$route.query.id}`)
	    	}
	    },
	    watch: {
	    	metadataInfo(value) {
				if (Object.keys(value).length > 0) {
					this.keys = Object.keys(value)
				}
			},
			metadataname(value) {
				this.params.name = `${this.$store.state.auth.username}_${this.name}_${value}_metadata`
			},
		},
	    computed: {
	        ...mapFields("base", [
	        	"baseURL",
	        	"name",
	            "metadataList",
	            "metadataInfo",
	        	"metadataname",
	        ]),
	        ...mapFields("auth", ["username"])
	    },
	    mounted() {
	    	this.$nextTick(() => {
 	           	this.$store.dispatch("base/MetadataList", {project_name: this.$route.query.name.split("_")[1]})
 	           	this.params.name = `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module}_metadata`
 	           	this.params.m_id = this.$route.query.id

 	           	this.$store.dispatch("base/MetadataInfo", this.params)
 	           	this.queryParams = true
	    		this.queryKeys = Object.keys(this.$route.query).pop().split(",")
	    		this.queryValues = this.$route.query[Object.keys(this.$route.query).pop()].split(",")
			})
	    },
	};
</script>