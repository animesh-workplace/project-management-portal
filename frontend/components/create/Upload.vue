<template>
	<div>
		<ElementsSubNavbar />
		<div class="grid grid-flow-col col-span-13">
			<div class="mt-6 px-8 flex justify-right grid grid-flow-col col-span-1">
		      <div class="box-content h-full w-64 p-4 border-4">
		      	<h1 class="text-xl">Sample Identifier</h1>
		        <a @click="getProjectConfig()"
		          :class="sample_identifier ? 'block no-underline text-sm py-1 transition-colors duration-200 ease-in-out hover:text-green-700 capitalize cursor-pointer pl-6 text-green-700' : 'block no-underline text-sm py-1 transition-colors duration-200 ease-in-out hover:text-green-700 capitalize cursor-pointer pl-6'"
		          >{{$route.query.name.split("_")[1]}}</a
		        >
		        <h1 class="text-xl">Metadata</h1>
		        <a v-for="event in metadataList.metadata" :key="event.id" @click="getMetadataConfig(event)"
		          :class="metadataColor != event ? 'block no-underline text-sm py-1 transition-colors duration-200 ease-in-out hover:text-green-700 capitalize cursor-pointer pl-6' : 'block no-underline text-sm py-1 transition-colors duration-200 ease-in-out hover:text-green-700 capitalize cursor-pointer pl-6 text-green-700'"
		          >{{ event }}</a
		        >
		      </div>
			</div>
			<div class="col-span-12 pt-4 pr-2 flex justify-right box-content h-full w-90 p-4 border-4">
				<form v-if="sample_identifier">
					<!-- <h2 class="text-2xl font-bold text-gray-800 text-left mb-5 border-black-500">
		              {{$route.query.name.split("_")[1]}}
		            </h2> -->
				    <div class="grid gap-6 mb-6 lg:grid-cols-1">
				        <div v-for="event in projectConfig">
				            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{event.name}}</label>
				            <input v-model="params[event.name.toLowerCase()]" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required v-if="event.data_type=='character'">
				            <input v-model="params[event.name.toLowerCase()]" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 9999999999" required v-if="event.data_type=='integer'">
							<div v-if="event.data_type=='radio'">
								<ul class="items-center w-full text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">
								    <li v-for="i in event.options" class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
								        <div class="flex items-center pl-3">
								            <input v-model="params[event.name.toLowerCase()]" id="horizontal-list-radio-license" type="radio" :value="i" name="list-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
								            <label for="horizontal-list-radio-license" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">{{i}}</label>
								        </div>
								    </li>
								</ul>
							</div>
							<div v-if="event.data_type=='multiradio'" v-for="i in event.options">
								<input type="checkbox" :id="i" :value="i" v-model="params[event.name.toLowerCase()]">
								<label for="jack">{{i}}</label>
							</div>
							<div v-if="event.data_type=='boolean'">
								<label class="block">
								  <select v-model="params[event.name.toLowerCase()]" class="form-select block w-full mt-1">
								    <option value="yes" :name="params[event.name.toLowerCase()]">Yes</option>
								    <option value="no" :name="params[event.name.toLowerCase()]">No</option>
								  </select>
								</label>
							</div>	
							<div class="text-gray-400 bg-white" v-if="event.data_type=='date'">
				              <input
				                v-model="params[event.name.toLowerCase()]"
				                class="shadow appearance-none border w-48 rounded py-2 px-3 bg-gray-100 text-gray-500 leading-tight focus:outline-none focus:shadow-outline text-sm"
				                :name="params[event.name.toLowerCase()]"
				                type="date"
				                placeholder="start_date"
				              />
				            </div>
							<div>
					            <textarea v-model="params[event.name]"
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
				    	<button @click="uploadProject()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit SI</button>
				</form>
				<form v-if="metadata">
				    <div class="grid gap-6 mb-6 lg:grid-cols-1">
				        <div v-for="event in metadataConfig">
				            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{event.name}}</label>
				            <input v-model="params[event.name.toLowerCase()]" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required v-if="event.data_type=='character'">
				            <input v-model="params[event.name.toLowerCase()]" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 9999999999" required v-if="event.data_type=='integer'">
							<div v-if="event.data_type=='radio'">
								<ul class="items-center w-full text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">
								    <li v-for="i in event.options" class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
								        <div class="flex items-center pl-3">
								            <input v-model="params[event.name.toLowerCase()]" :id="event.name" type="radio" :value="i" :name="event.name" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
								            <label :for="event.name" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">{{i}}</label>
								        </div>
								    </li>
								</ul>
							</div>
							<div v-if="event.data_type=='multiradio'" v-for="i in event.options" class="grid-rows-1">
								<input type="checkbox" :id="i" :value="i" v-model="params[event.name.toLowerCase()]">
								<label :for="i">{{i}}</label>
							</div>
							<div v-if="event.data_type=='boolean'">
								<label class="block">
								  <select v-model="params[event.name.toLowerCase()]" class="form-select block w-full mt-1">
								    <option value="yes" :name="params[event.name.toLowerCase()]">Yes</option>
								    <option value="no" :name="params[event.name.toLowerCase()]">No</option>
								  </select>
								</label>
							</div>	
							<div class="text-gray-400 bg-white" v-if="event.data_type=='date'">
				              <input
				                v-model="params[event.name.toLowerCase()]"
				                class="shadow appearance-none border w-48 rounded py-2 px-3 bg-gray-100 text-gray-500 leading-tight focus:outline-none focus:shadow-outline text-sm"
				                :name="params[event.name.toLowerCase()]"
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
				    	<button @click="uploadMetadata()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
				</form>
			</div>
	    </div>
	</div>
</template>
<script type="text/javascript">
	import { mapFields } from "vuex-map-fields";
	export default {
		data: () => ({
			metadataColor: "",
			metadata_name: "",
			sample_identifier: true,
			metadata: false,
			params: {},
		}),
		computed: {
			...mapFields("base", ["metadataList", "projectConfig", "metadataConfig"]),
			...mapFields("auth", ["username"])
		},
		watch: {
			// projectConfig(value) {
			// 	let temp = {}
			// 	value.forEach(function (item, index) {
			// 	  if (item.data_type == "multiradio") {
			// 	  	temp[item.name.toLowerCase()] = []
			// 	  } else {
			// 	  	temp[item.name.toLowerCase()] = ""
			// 	  }
			// 	});
			// 	this.params = temp
			// 	console.log("lower",this.params)
			// },
			// metadataConfig(value) {
			// 	let temp = {}
			// 	value.forEach(function (item, index) {
			// 	  if (item.data_type == "multiradio") {
			// 	  	temp[item.name.toLowerCase()] = []
			// 	  } else {
			// 	  	temp[item.name.toLowerCase()] = ""
			// 	  }
			// 	});
			// 	this.params = temp
			// },
		},
		methods: {
			async getProjectConfig() {
				this.metadata = false
				this.metadataColor = ""
				this.sample_identifier = true
				await this.$store.dispatch('base/ProjectConfig', {name: this.$route.query.name.split("_")[1]})
				const temp = {}
				this.projectConfig.forEach(function (item, index) {
				  if (item.data_type == "multiradio") {
				  	temp[item.name.toLowerCase()] = []
				  } else {
				  	temp[item.name.toLowerCase()] = ""
				  }
				});
				this.params = temp
			},
			async getMetadataConfig(value) {
				this.metadataColor = value
				this.metadata = true
				this.sample_identifier = false
				this.metadata_name = value
				this.$router.push({path: '/create/upload/', query: {
									name: this.$route.query.name,
									metadata: this.metadata_name
								}})
				await this.$store.dispatch('base/MetadataConfig', {project: this.$route.query.name.split("_")[1], name: value})
				let temp = {}
				this.metadataConfig.forEach(function (item, index) {
				  if (item.data_type == "multiradio") {
				  	temp[item.name.toLowerCase()] = []
				  } else {
				  	temp[item.name.toLowerCase()] = ""
				  }
				});
				this.params = temp
			},
			async uploadProject() {
				this.$store.dispatch('base/UploadProject', {name: this.$route.query.name, data: [this.params]})
			},
			async uploadMetadata() {
				this.$store.dispatch('base/UploadMetadata', {name: `${this.username}_${this.$route.query.name.split("_")[1]}_${this.metadata_name}_metadata`.toLowerCase(), data: [this.params]})
			}
		},
		mounted() {
	    	this.$nextTick(() => {
	    		this.$store.dispatch('base/MetadataList', {project_name: this.$route.query.name.split("_")[1]})
	    		this.$store.dispatch('base/ProjectConfig', {name: this.$route.query.name.split("_")[1]})
			})
	    },
	}
</script>