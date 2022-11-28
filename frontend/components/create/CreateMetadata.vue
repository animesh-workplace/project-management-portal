<template>
	<div>
		<div class=" grid grid-cols-1 gap-4 place-items-center">
			<form>
			    <!-- <h1 class='text-center text-xl font-bold'>Model Schema</h1> -->
			    <div>
			    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Project Name</label>
		            <input v-model="params.project" type="text" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
		        </div>
		        <h1 class='text-center text-xl font-bold'>Create metadata</h1>
		        <div>
			    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Metadata Name</label>
		            <input v-model="params.name" type="text" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
		        </div>

		        <div v-for="(element, index) in params.config">
		        	<h2 class='text-center text-xl font-bold mt-2' id="field1">Data register {{index+1}}</h2>
				    <div>
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Fieldname</label>
			            <input v-model="element['name']" name="name" type="text" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
			        </div>

				    <div class="flex justify-left">
					  <div class="mb-3 mt-2 xl:w-full">
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Datatype <a class="text-xs font-thin">(default CharField)</a></label>
					    <select v-model="element['data_type']" class="form-select
					      block
					      w-full
					      px-3
					      py-2.5
					      text-base
					      font-normal
					      text-gray-700
					      bg-white bg-clip-padding bg-no-repeat
					      border border-solid border-gray-300
					      rounded
					      transition
					      ease-in-out
					      m-0
					      focus:text-gray-700 focus:bg-white focus:border-gray-600 focus:outline-none" aria-label="Default select example">
					      	<option value="character" selected>CharField</option>
					        <option value="date">DateTimeField</option>
					        <option value="radio" id="radio">Radio</option>
					        <option value="multiradio">Multi-radio</option>
					        <option value="integer">IntegerField</option>
					        <option value="float">FloatField</option>
					        <option value="boolean">BooleanField</option>
					        <option value="text">TextField</option>
					    </select>
					  </div>
					</div>
					<div v-if="((element['data_type']=='multiradio') || (element['data_type']=='radio'))">
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Options</label>
			    		<div class="grid grid-cols-2">
		            		<input v-for="(e,i) in element['options']" v-model="element['options'][i]['value']" name="name" type="text" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
			    		</div>
						<button v-if="((element['data_type']=='multiradio') || (element['data_type']=='radio'))" class="text-white bg-gray-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-1 py-1.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" @click="onOptions(element)" type="button">+ Add option</button>
			        </div>

				    <div>
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Maximum length <a class="text-xs font-thin">(default 225)</a></label>
			            <input v-model="element['max_length']" type="number" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="1234" required>
			        </div>

				    <div class="flex justify-left">
					  <div class="mb-3 mt-2 xl:w-full">
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Null field <a class="text-xs font-thin">(default False)</a></label>
					    <select v-model="element['null']" class="form-select
					      block
					      w-full
					      px-3
					      py-2.5
					      text-base
					      font-normal
					      text-gray-700
					      bg-white bg-clip-padding bg-no-repeat
					      border border-solid border-gray-300
					      rounded
					      transition
					      ease-in-out
					      m-0
					      focus:text-gray-700 focus:bg-white focus:border-gray-600 focus:outline-none" aria-label="Default select example">
					      	<option value="False" selected>False</option>
					        <option value="True">True</option>
					    </select>
					  </div>
					</div>

				    <div class="flex justify-left">
					  <div class="mb-3 xl:w-full">
				    	<label class="block text-sm font-medium text-gray-900 dark:text-gray-300">Unique <a class="text-xs font-thin">(default False)</a></label>
					    <select v-model="element['unique']" class="form-select
					      block
					      w-full
					      px-3
					      py-2.5
					      text-base
					      font-normal
					      text-gray-700
					      bg-white bg-clip-padding bg-no-repeat
					      border border-solid border-gray-300
					      rounded
					      transition
					      ease-in-out
					      m-0
					      focus:text-gray-700 focus:bg-white focus:border-gray-600 focus:outline-none" aria-label="Default select example" :name="element['unique']">
					      	<option value="False" :name="element['unique']" selected>False</option>
				        	<option value="True">True</option>
					    </select>
					  </div>
					</div>
		        </div>

			    <button @click="onClick()" type="button" id="buttonArea" class="text-white bg-gray-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add field</button>
			    <div class="mt-2" id="buttonArea">
			      <button @click="createMeatadata()" type="button" id="buttonArea" class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-90 sm:w-auto px-44 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
			    </div>
			</form>
		</div>
	</div>
</template>
<script type="text/javascript">
	export default {
		data: () => ({
			params: {
				name: "",
				project: "",
				config: [{"name": "", "data_type": "character", "max_length": 225, "null": "False", "unique": "False", "options": [{"value": ""}]}],
			},
		}),
		methods: {
			onClick() {
				let temp = {"name": "", "data_type": "character", "max_length": 225, "null": "False", "unique": "False", "options": [{"value": ""}]}
				this.params.config.push(temp)
			},
			onOptions(temp) {
				temp["options"].push({"value": ""})
			},
			async createMeatadata() {
				this.params.config.forEach(function(e,i) {
					let optionLists = []
					if ((e.data_type == "radio") || (e.data_type == "multiradio")) {
					    for (const [ key, value ] of Object.entries(e.options)) {
					        optionLists.push(value["value"])
					    }
					    e.options = optionLists
					}
				})
				await this.$store.dispatch("base/CreateMetadata", this.params);
			},
		}
	}
</script>