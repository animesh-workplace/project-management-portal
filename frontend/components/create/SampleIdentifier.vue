<template>
	<div>
		<div
		  class="w-full flex sm:border-b sm:border-gray-300 relative flex-col sm:flex-row justify-items-center"
		>
		  <div @click="isProject()"
		    class="flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 false"
		  >
		    Sample Identifier
		  </div>
		  <div @click="isMetadata()"
		    class="flex-1 sm:text-center font-medium pb-3 cursor-pointer hover:text-green-400 false"
		  >
		    Metadata
		  </div>
		  <div
		    :class="project ? 'hidden sm:block absolute bottom-0 left-0 h-1 bg-green-400 transition-transform duration-300 ease-out w-1/2 transform translate-x-double' : 'hidden sm:block absolute bottom-0 right-0 h-1 bg-green-400 transition-transform duration-300 ease-out w-1/2 transform translate-x-double'"
		  ></div>
		</div>
		<div class="max-w-6xl mx-auto bg-gray-100 p-16">
			<div :class="metadata ? 'hidden' : ''">
				<CreateProject />
			</div>
			<div :class="project ? 'hidden' : ''">
				<CreateMetadata />
			</div>
			<!-- <form action="" :class="metadata ? 'hidden' : ''">
			    <div class="grid gap-6 mb-6 lg:grid-cols-1">
			        <div>
			            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Project Name</label>
			            <input v-model="params.name" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
			        </div>
			        <div>
			            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Config</label>
			            <textarea v-model="params.config"
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
					      placeholder="Your json data" required
					    ></textarea>
			        </div>
			    </div>
			    	<button @click="createProject()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
			</form>
			<form action="" :class="project ? 'hidden' : ''">
			    <div class="grid gap-6 mb-6 lg:grid-cols-1">
			        <div>
			            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Project Name</label>
			            <input v-model="params.project" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Test" required>
			        </div>
			        <div>
			            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Metadata Name</label>
			            <input v-model="params.name" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Dna" required>
			        </div>
			        <div>
			            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Config</label>
			            <textarea v-model="params.config"
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
					      placeholder="Your json data" required
					    ></textarea>
			        </div>
			    </div>
			    	<button @click="createMetadata()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
			</form> -->
		</div>
	</div>
</template>
<script type="text/javascript">
	export default {
		data: () => ({
			metadata: false,
			project: true,
			// params: {
			// 	name: "",
			// 	project: "",
			// 	config: null
			// }
		}),
		methods: {
			// async createProject() {
			// 	const data = {
		 //            name: this.params.name,
		 //            config: JSON.parse(this.params.config)
		 //         };
			//     this.$store.dispatch("base/CreateSampleIdentifier", data);
	  //       },
	  //       async createMetadata() {
			// 	const data = {
			// 		project: this.params.project,
		 //            name: this.params.name,
		 //            config: JSON.parse(this.params.config)
		 //         };
			//     this.$store.dispatch("base/CreateMetadata", data);
	  //       },
	        async isMetadata() {
	        	this.metadata = true
	        	this.project = false
	        },
	        async isProject() {
	        	this.project = true
	        	this.metadata = false
	        }
		}
	}
</script>