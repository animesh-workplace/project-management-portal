<template>
	<div>
		<form>
			<h2 class="text-2xl font-bold text-gray-800 text-left mb-5">
	            Bulk upload
	        </h2>
			<div class="grid grid-flow-col col-span-2 gap-2">
			  <label class="block shadow">
			    <span class="sr-only">Choose File</span>
			    <input type="file" id="file" ref="file" class="block w-full text-sm text-gray-500 file:py-2 file:px-6 file:rounded file:border-1 file:border-gray-400"/>
			  </label>
			  <button @click="csvToJson()" type="button" class="bg-gray-700 text-white rounded-md text-sm w-20">Add file</button>
			</div>
		  	<button @click="uploadSample()" type="button" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit SI</button>
		  	<a @click="downloadFile()"
                target="_blank"
                class="text-blue-600 dark:text-blue-500 hover:underline cursor-pointer ml-12"
                >Click here to dounload sample template</a
            >
		</form>
	</div>
</template>
<script type="text/javascript">
	import papa from "papaparse"
	import { mapFields } from "vuex-map-fields";
	export default {
		data: () => ({
			csvData: [],
			params: {},
			newData: []
		}),
		computed: {
			...mapFields("base", ["metadataList", "projectConfig", "metadataConfig"]),
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
			},
			async uploadSample() {
				const keys = this.csvData.shift();
				this.newData = this.csvData.map(values => Object.fromEntries(keys.map((key, idx) => [
					key.toLowerCase(),
					values[idx]
				])));
				await this.$store.dispatch('base/UploadProject', {name: this.$route.query.name, data: this.newData})
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