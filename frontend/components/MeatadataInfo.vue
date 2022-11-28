<template>
	<div>
		<ElementsSubNavbar />
		<div
	      v-show="isShowing"
	      class="fixed inset-10 w-2/3 h-4 mx-auto pt-80 py-16 mr-36 grid justify-center z-30"
	      id="my-modal"
	    >
	      <div v-show="isShowing" class="w-full shadow p-5 rounded-lg bg-gray-50">
			<p class="font-bold flex justify-center">Sure you want to delete</p>
			<div class="flex justify-center items-center">
			    <div class="mx-auto grid gap-6 mb-6 lg:grid-cols-2 w-80 flex justify-center items-center">
			        <button @click="cancelDelete()"
		                class="px-10 py-2 mt-8 font-semibold text-sm bg-red-400 hover:bg-red-500 text-white items-center rounded-full shadow-sm"
		            >
		                No..
		            </button>
		            <button @click="deleteMeatadata()"
		                class="px-10 py-2 mt-8 font-semibold text-sm bg-blue-400 text-white rounded-full shadow-sm hover:bg-blue-500"
		            >
		                Yes
		            </button>
			    </div>
			</div>
	      </div>
	    </div>
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
		<div v-if="view" class="mx-auto flex items-center mt-4">
			<div class="mx-auto grid gap-6 mb-6 lg:grid-cols-4 flex justify-center items-center">
		        <div v-for="event in keys.slice(1,)">
		            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300 capitalize">{{event.replaceAll("_"," ")}}</label>
		            <input type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 capitalize" :value="metadataInfo[event]" readonly>
		        </div>
		    </div>
		</div>
		<div v-if="edit" class="flex items-center mt-4">
				<div class="mx-auto grid gap-6 mb-6 lg:grid-cols-1 flex justify-center items-center">
					<form>
					    <div class="grid gap-6 mb-6 lg:grid-cols-4">
					        <div v-for="event in metadataConfig">
					            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{event.name}}</label>
					            <input v-model="editData[event.name.toLowerCase()]" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" :name="editData[event.name.toLowerCase()]" placeholder="Test" required v-if="event.data_type=='character'">
					            <input v-model="editData[event.name.toLowerCase()]" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 9999999999" required v-if="event.data_type=='integer'">
								<div v-if="event.data_type=='radio'">
									<ul class="items-center w-full text-sm font-medium text-gray-900 rounded-lg border border-gray-200 sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">
									    <li v-for="i in event.options" class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
									        <div class="flex items-center pl-3">
									            <input v-model="editData[event.name.toLowerCase()]" :id="event.name" type="radio" :value="i" :name="event.name" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
									            <label :for="event.name" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">{{i}}</label>
									        </div>
									    </li>
									</ul>
								</div>
								<div v-if="event.data_type=='multiradio'" v-for="i in event.options" class="grid-rows-1">
									<input type="checkbox" :id="i" :value="i" v-model="editData[event.name.toLowerCase()]">
									<label :for="i">{{i}}</label>
								</div>
								<div v-if="event.data_type=='boolean'">
									<label class="block">
									  <select v-model="editData[event.name.toLowerCase()]" class="form-select block w-full mt-1">
									    <option value="yes" :name="editData[event.name.toLowerCase()]">Yes</option>
									    <option value="no" :name="editData[event.name.toLowerCase()]">No</option>
									  </select>
									</label>
								</div>	
								<div class="text-gray-400" v-if="event.data_type=='date'">
					              <input v-if="editData"
					                v-model="editData[event.name.toLowerCase()]" 
					                class="shadow appearance-none border w-full rounded py-2 px-3 bg-gray-100 text-gray-500 leading-tight focus:outline-none focus:shadow-outline text-sm"
					                :name="editData[event.name.toLowerCase()]"
					                type="date"
					                placeholder="start_date"
					              />
					            </div>
								<div>
						            <textarea v-model="params[event.name.toLowerCase()]"
								      class="
								        form-control
								        block
								        w-full
								        px-3
								        py-1.5
								        text-base
								        font-normal
								        text-gray-700
								        bg-white bg-clip-padding
								        border border-solid border-gray-300
								        rounded
								        transition
								        ease-in-out
								        m-0
								        focus:text-gray-700 focus:bg-white focus:border-gray-900 focus:outline-none
								      "
								      id="exampleFormControlTextarea1"
								      rows="3"
								      placeholder="Your json data" required v-if="event.data_type=='text'"
								    ></textarea>
						        </div>
					        </div>
					    </div>
					    	<button @click="editMetdata()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
					    	<button @click="cancelEdit()" type="button" class="text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-red-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Cancel</button>
					</form>
				</div>
			</div>
		<div v-if="Object.values(metadataInfo)[0] != '' && showEditmetadata == true" class="flex justify-center items-center">
		    <div class="mx-auto grid gap-6 mb-6 lg:grid-cols-2 w-80 flex justify-center items-center">
	            <button @click="veiwDeletePage()"
	                class="px-10 py-2 mt-8 font-semibold text-sm bg-red-600 hover:bg-red-500 text-white rounded-full shadow-sm"
	            >
	                Delete
	            </button>
		        <button @click="editMetdataForm()"
	                class="px-10 py-2 mt-8 font-semibold text-sm bg-green-400 hover:bg-green-600 text-white rounded-full shadow-sm"
	            >
	                Edit
	            </button>
		    </div>
		</div>
	</div>
</template>
<script>
	import { mapFields } from "vuex-map-fields";
	import moment from "moment";
	export default {
	    data: () => ({
	    	isShowing: false,
	    	view: true,
	    	edit: false,
	    	queryParams: "",
	    	queryKeys: [],
	    	queryValues: [],
	    	params: {
	    		name: "",
	    		m_id: 1
	    	},
	    	keys: [],
	    	editData: {},
	    	date: "2022-08-07",
	    	showEditmetadata: true
	    }),


	    methods: {
	    	async metaData(value) {
	    		this.view = true
	    		this.edit = false
	    		this.params.name = `${this.username}_${this.$route.query.name.split('_')[1]}_${value}_metadata`
	    		this.params.m_id = this.$route.query.id
	    		this.$store.dispatch("base/MetadataInfo", this.params)
	    		this.editData = this.metadataInfo
	    		this.$store.dispatch("base/MetadataConfig", {project: this.$route.query.name.split("_")[1], name: value.toLowerCase()})
	    		this.$router.push(`/metadatainfo?name=${this.$route.query.name}&module=${value}&id=${this.$route.query.id}&${Object.keys(this.$route.query).pop()}=${Object.values(this.$route.query).pop()}`)
	    	},
	    	async editMetdataForm() {
	    		this.view = false
	    		this.edit = true
	    		this.showEditmetadata = false
	    		this.params.name = `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module}_metadata`
 	           	this.params.m_id = this.$route.query.id
	    		this.$store.dispatch("base/MetadataInfo", this.params)
	    		this.editData = this.metadataInfo
	    		this.$store.dispatch("base/MetadataConfig", {project: this.$route.query.name.split("_")[1], name: this.$route.query.module.toLowerCase()})
	    	},
	    	async editMetdata() {
	    		const pk = this.editData.id
	    		delete this.editData.id
	    		await this.$store.dispatch("base/UpdateMetadata", {name: `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module.toLowerCase()}_metadata`, pk: pk, data: [this.editData]})
	    		await this.$store.dispatch("base/MetadataInfo", this.params)
	    		this.view = true
	    		this.edit = false
	    		this.showEditmetadata = true
	    	},
	    	veiwDeletePage() {
	    		this.isShowing = true
	    	},
	    	cancelDelete() {
				this.isShowing = false
			},
			async cancelEdit() {
				this.showEditmetadata = true
				this.view = true
	    		this.edit = false
			},
			async deleteMeatadata() {
				await this.$store.dispatch("base/DeleteMetadata", {"name": `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module.toLowerCase()}_metadata`, "pk": this.queryValues[0]})
				this.isShowing = false
				this.$store.dispatch("base/MetadataInfo", this.params)
			},
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
	        	"name",
	            "metadataList",
	            "metadataInfo",
	        	"metadataname",
	        	"metadataConfig",
	        ]),
	        ...mapFields("auth", ["username"])
	    },
	    async mounted() {
	    	await this.$nextTick(() => {
	    		if (this.$route.query.name) {
	 	           	this.$store.dispatch("base/MetadataList", {project_name: this.$route.query.name.split("_")[1]})
	 	           	this.params.name = `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module}_metadata`
	 	           	this.params.name = `${this.username}_${this.$route.query.name.split('_')[1]}_${this.metadataname}_metadata`
	 	           	this.params.m_id = this.$route.query.id

	 	           	this.$store.dispatch("base/MetadataInfo", {name: `${this.$route.query.name.split("_")[0]}_${this.$route.query.name.split("_")[1]}_${this.$route.query.module}_metadata`, m_id: this.$route.query.id})
		    		this.editData = this.metadataInfo
	 	           	this.queryParams = true
		    		this.queryKeys = Object.keys(this.$route.query).pop().split(",")
		    		this.queryValues = this.$route.query[Object.keys(this.$route.query).pop()].split(",")
	    		}
			})
	    },
	};
</script>