<template>
	<div>
		<div
	      v-show="isShowing"
	      class="fixed inset-10 w-full h-4 pt-24 py-16 mr-40 pr-80 pl-80 grid justify-center z-30"
	      id="my-modal"
	    >
	    	<div class="mx-auto w-full flex justify-center items-center bg-gray-50">
		    	<div :class="toggleUploadUpdate && (projectDataToUpdate.length == 0 || projectDataToUpload.length == 0) ? 'mx-auto grid gap-6 lg:grid-cols-1 w-full flex justify-center items-center' : 'mx-auto grid gap-6 lg:grid-cols-2 w-full flex justify-center items-center'">
			    	<div v-if="projectDataToUpdate.length>0" class="w-full shadow p-5 rounded-lg bg-gray-50">
			    		<div class="grid justify-items-end">
				        	<svg v-on:click="isUpdateRemove = false; toggleUploadUpdate=false" class="w-8 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>
				        </div>
		    			<p class="w-full flex sm:border-b sm:border-gray-300 relative flex-col sm:flex-row text-xl font-bold flex justify-center">Data to be updated</p>
					    <table v-if="isUpdateRemove" class="w-full divide-y divide-gray-200 table-fixed dark:divide-gray-700">
							<thead>
							    <tr>
							      <th>{{updateKeys[0]}}</th>
							    </tr>
							</thead>
							<tbody>
							    <tr class="hover:bg-gray-100 dark:hover:bg-gray-700 text-center" v-for="event in projectDataToUpdate" :key="event.id">
							      {{event[updateKeys[0]]}}</td>
							    </tr>
							 </tbody>
						</table>
			    	</div>
			    	<div v-if="projectDataToUpload.length>0" class="w-full shadow p-5 rounded-lg bg-gray-50">
			    		<div class="grid justify-items-end">
				        	<svg v-on:click="isUploadRemove = false; toggleUploadUpdate=false" class="w-8 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>
				        </div>
		    			<p class="text-xl font-bold flex justify-center">Data to be uploaded</p>
					    <table v-if="isUploadRemove" class="w-full divide-y divide-gray-200 table-fixed dark:divide-gray-700">
							<thead>
							    <tr>
							      <th>{{uploadKeys[0]}}</th>
							    </tr>
							</thead>
							<tbody>
							    <tr class="hover:bg-gray-100 dark:hover:bg-gray-700 text-center" v-for="event in projectDataToUpload" :key="event.id">
							      {{event[uploadKeys[0]]}}</td>
							    </tr>
							 </tbody>
						</table>
			    	</div>
		    	</div>
	    	</div>
	    	<div class="mx-auto grid gap-6 mb-6 lg:grid-cols-2 w-full flex justify-center items-center">
			    <button @click="cancelProjectUpdate()" type="button" class="mt-2 text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">Cancel</button>
				<button :loading="loader" @click="bulkProjectUpdate()" type="button" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
			</div>
		</div>
		<form>
			<h2 class="text-2xl font-bold text-gray-800 text-left mb-5">
	            Bulk upload
	        </h2>
			<div class="grid grid-flow-col col-span-2 gap-2 w-80 bg-gray-200">
			  <label class="block shadow">
			    <span class="sr-only">Choose File</span>
			    <input @change="csvToJson()" type="file" id="file" ref="file" class="block w-full text-sm text-gray-500 file:py-2 file:px-6 file:rounded file:border-1 file:border-gray-400"/>
			  </label>
			  <!-- <button @click="bulkProjectUpdate()" type="button" class="bg-gray-700 text-white rounded-md text-sm w-20">Add file</button> -->
			</div>
		  	<button @click="uploadSample()" type="button" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit SI</button>
		  	<a @click="downloadFile()"
                target="_blank"
                class="text-blue-600 dark:text-blue-500 hover:underline cursor-pointer ml-12"
                >Click here to download sample template</a
            >
		</form>
	</div>
</template>
<script type="text/javascript">
	// import fs from 'fs';
	import * as fs from 'fs-promise';
	import papa from "papaparse"
	import { mapFields } from "vuex-map-fields";
	export default {
		data: () => ({
			isUploadRemove: true,
			isUpdateRemove: true,
			toggleUploadUpdate: true,
			loader: false,
			loader_option: {
				lineWidth: 3,
				fontSize: 14,
				color: 'black',
				text: 'Loading',
				fontWeight: 500,
				maskColor: '#f6f8f9',
				fontFamily: 'Averta',
			},
			params: {},
			csvData: [],
			newData: [],
			csvData1: [],
			toUpload: [],
			updateKeys: [],
			uploadKeys: [],
			isShowing: false,
			project_config: []
		}),
		watch: {
			projectDataToUpdate(value) {
				if (Object.keys(value).length > 0) {
					this.updateKeys = Object.keys(value[0])
				} else {
					this.updateKeys= []
				}
			},
			projectDataToUpload(value) {
				if (Object.keys(value).length > 0) {
					this.uploadKeys = Object.keys(value[0])
				} else {
					this.uploadKeys = []
				}
				// this.toUpload = val
			},
			projectConfig(value) {
				this.project_config = value
			}
		},
		computed: {
			...mapFields("base", ["metadataList", "projectConfig", "metadataConfig","projectDataToUpload", "projectDataToUpdate"]),
			...mapFields("auth", ["username"])
		},
		methods: {
			async csvToJson() {
				let csvFile = this.$refs.file.files[0]
				if(csvFile == undefined){
					this.$notification.show('File not found','Please select the file', 'WARNING')
					this.csvData = []
					return;
				}
				let that = this
					papa.parse(csvFile, {
						headers: true,
						dynamicTyping: true,
						skipEmptyLines: true,
						complete(result){
							that.csvData=result.data
						}
					})
				console.log(this.csvData)
			},
			async uploadSample() {
				let csvFile = this.$refs.file.files[0]
				if(csvFile == undefined){
					this.$notification.show('File not found','Please select the file', 'WARNING')
					this.csvData = []
					return;
				}
				let that = this
					papa.parse(csvFile, {
						headers: true,
						dynamicTyping: true,
						skipEmptyLines: true,
						complete(result){
							that.csvData=result.data
						}
					})
				console.log(this.csvData)
				const keys = this.csvData.shift();
				this.newData = this.csvData.map(values => Object.fromEntries(keys.map((key, idx) => [
					key.toLowerCase(),
					values[idx]
				])));
				await this.$store.dispatch('base/SeperateProjectData', {name: this.$route.query.name, data: this.newData})
				let uploadto = JSON.parse(JSON.stringify(this.projectDataToUpload))

				// this.project_config.forEach(function(n){
				//     if(n["data_type"]=="filefield"){
				//     	uploadto.forEach(function(i){
				// 		    i[n["name"]] = new File([`${n["name"]}`], i[n["name"]],{type: "text/csv",});
				//     	})
				//     }
				// })
				// this.toUpload = uploadto[0]
				// console.log(this.toUpload)
				
				// var fs = require("fs");
				console.log(fs)
				try {
				  const data = fs.readFile('/home/nsm-07/Downloads/Hotel_Bookings.csv', 'utf8');
				  await console.log(data);
				} catch (err) {
				  console.error(err);
				}
				// fs.readFile('/home/nsm-07/Downloads/Hotel_Bookings.csv', function (err, data) {
				//    if (err) {
				//       return console.error(err);
				//    }
				//    console.log("Asynchronous read: " + data.toString());
				// });
				// console.log(fs)
				// var data = fs.FileReadStream('/home/nsm-07/Downloads/Hotel_Bookings.csv');
				// console.log("Synchronous read: " + data.toString());
				// console.log(fs.readFile('/home/nsm-07/Downloads/Hotel_Bookings.csv', 'utf8'));

				// let csvFile1 = "/home/nsm-07/Downloads/Hotel_Bookings.csv"
				// if(csvFile1 == undefined){
				// 	this.$notification.show('File not found','Please select the file', 'WARNING')
				// 	this.csvData1 = []
				// 	return;
				// }
				// let that1 = this
				// 	papa.parse(csvFile1, {
				// 		headers: true,
				// 		dynamicTyping: true,
				// 		skipEmptyLines: true,
				// 		complete(result){
				// 			that1.csvData1=result.data
				// 		}
				// 	})
				// console.log("csv data",this.csvData1)

				// const reader = new FileReader();
				// reader.onload = (evt) => {
				//   console.log("data",this.toUpload["file"].target.result);
				// };
				// reader.readAsText(this.toUpload["file"]);
				// console.log(reader)
				// console.log(this.toUpload["file"])
				this.isShowing = true
			},
			async bulkProjectUpdate() {
				this.loader = true
				let uploadformData = new FormData()
				uploadformData.append("name", this.$route.query.name)
				Object.keys(this.toUpload).forEach(key => uploadformData.append(key, this.toUpload[key]));
				console.log(uploadformData)
				if (this.projectDataToUpdate.length == 0) {
					this.isUpdateRemove = false
				} else if (this.projectDataToUpload.length == 0) {
					this.isUploadRemove = false
				}
				if (this.projectDataToUpdate.length > 0 || this.projectDataToUpload.length > 0) {
					if (this.isUpdateRemove && this.isUploadRemove) {
						await this.$store.dispatch('base/BulkUpdateProject', {name: this.$route.query.name, data: this.projectDataToUpdate})
						await this.$store.dispatch('base/UploadProject', uploadformData)
					} else if (this.isUploadRemove) {
						await this.$store.dispatch('base/UploadProject', uploadformData)
					} else if (this.isUpdateRemove) {
						await this.$store.dispatch('base/BulkUpdateProject', {name: this.$route.query.name, data: this.projectDataToUpdate})
					}
				}
				this.loader = false
				this.isShowing = false
				this.isUploadRemove = true
				this.isUpdateRemove = true
				this.toggleUploadUpdate = true
			},
			cancelProjectUpdate() {
				this.isShowing = false
				this.isUploadRemove = true
				this.isUpdateRemove = true
				this.toggleUploadUpdate = true
			},
			async downloadFile() {
		      const csv = await this.$axios.post(`http://10.10.6.87/pmp/api/schema/projects/template/`, {name: this.$route.query.name.split("_")[1]})
		      console.log(csv)
		      const file_name = csv.data.split("/").at(-1);
		      const download_path = `http://10.10.6.87/pmp/api/project/download/${file_name}`;
		      this.$axios({
		        url: download_path,
		        method: 'GET',
		        responseType: 'blob',
		      }).then((response) => {
		        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
		        var fileLink = document.createElement('a');

		        fileLink.href = fileURL;
		        fileLink.setAttribute('download', file_name);
		        document.body.appendChild(fileLink);
		        fileLink.click();
		      });
		    },
		},
	}
</script>