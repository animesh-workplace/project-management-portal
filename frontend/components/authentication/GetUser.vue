<template>
	<div class="flex items-center">
	  <div>
	  	<!-- <strong>{{ profile }}</strong> -->
	    <strong>{{ profile.username }}</strong>
	    <strong>{{ profile.email }}</strong>
	    <strong>{{ profile.first_name }}</strong>
	    <strong>{{ profile.last_name }}</strong>
	    <strong>{{ profile.bio }}</strong>
	    <strong>{{ profile.city }}</strong>
	    <strong>{{ profile.state }}</strong>
	    <strong>{{ profile.address }}</strong>
	    <strong>{{ profile.pin_code }}</strong>
	    <strong>{{ profile.institute }}</strong>
	    <strong>{{ profile.birth_date }}</strong>
	    <strong>{{ profile.job_profile }}</strong>
	    <strong>{{ profile.user_type }}</strong>
	    <span>Technical advisor</span>
	  </div>
	</div>
</template>

<script>
	import { mapFields } from "vuex-map-fields";
	export default {
	    data: () => ({
	        // params: {}
	    }),
	    computed: {
	        ...mapFields("auth", [
	            "username",
	            "profile",
	        ]),
	    },

	    mounted() {
	      	this.$nextTick(() => {
	           this.$store.dispatch("auth/GetUser")
	        });
	    },
	};
</script>