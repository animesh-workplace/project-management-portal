<template>
	<div>
		<div class="col-span-12 pt-4 pr-2 flex justify-right box-content h-full w-90 p-4 border-4 grid grid-flow-col col-span-2">
				<div>
					<form>
					    <div class="grid gap-6 mb-6 lg:grid-cols-1">
					        <div v-for="event in projectConfig">
					            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{event.name}}</label>
					            <input v-model="result[event.name.toLowerCase()]" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required v-if="event.data_type=='character'">
					            <input v-model="result[event.name.toLowerCase()]" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 9999999999" required v-if="event.data_type=='integer'">
								<div v-if="event.data_type=='radio'">
									<ul class="items-center w-full text-sm font-medium text-gray-900 rounded-lg border border-gray-200 sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">
									    <li v-for="i in event.options" class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
									        <div class="flex items-center pl-3">
									            <input v-model="result[event.name.toLowerCase()]" id="horizontal-list-radio-license" type="radio" :value="i" name="list-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
									            <label for="horizontal-list-radio-license" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">{{i}}</label>
									        </div>
									    </li>
									</ul>
								</div>
								<div v-if="event.data_type=='multiradio'" v-for="i in event.options">
									<input type="checkbox" :id="i" :value="i" v-model="result[event.name.toLowerCase()]">
									<label for="jack">{{i}}</label>
								</div>
								<div v-if="event.data_type=='boolean'">
									<label class="block">
									  <select v-model="result[event.name.toLowerCase()]" class="form-select block w-full mt-1">
									    <option value="yes" :name="result[event.name.toLowerCase()]">Yes</option>
									    <option value="no" :name="result[event.name.toLowerCase()]">No</option>
									  </select>
									</label>
								</div>	
								<div class="text-gray-400 bg-white" v-if="event.data_type=='date'">
					              <input
					                v-model="result[event.name.toLowerCase()]"
					                class="shadow appearance-none border w-48 rounded py-2 px-3 bg-gray-100 text-gray-500 leading-tight focus:outline-none focus:shadow-outline text-sm"
					                :name="result[event.name.toLowerCase()]"
					                type="date"
					                placeholder="start_date"
					              />
					            </div>
								<div>
						            <textarea v-model="result[event.name]"
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
					    <button @click="updateSI()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit SI</button>
					</form>
				</div>
			</div>
	</div>
</template>
<script type="text/javascript">
	// import * as d3 from 'd3';
	import { mapFields } from "vuex-map-fields";
	export default {
		data: () => ({
			result: {},
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
		methods: {
			async updateSI() {
				this.params["name"] = this.$route.query.name
				this.params["pk"] = this.$route.query.id
				delete this.result.id
				this.params["data"] = [this.result]
				await this.$store.dispatch("base/UpdateProject", this.params)
				this.$router.push(`/?name=${this.$route.query.name}`)
			},
		},
		mounted() {
			let queryKeys = Object.keys(this.$route.query).pop().split(",")
	    	let queryValues = this.$route.query[Object.keys(this.$route.query).pop()].split(",")
			queryKeys.forEach((key, i) => this.result[key] = queryValues[i]);
			this.params["name"] = this.$route.query.name
			this.params["pk"] = this.$route.query.id
			
			this.params["data"] = [this.result]
			console.log(this.params)
	    	this.$nextTick(() => {
	    		this.$store.dispatch('base/ProjectConfig', {name: this.$route.query.name.split("_")[1]})
			})
	    },
	}
</script>