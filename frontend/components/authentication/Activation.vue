<template>
	<div class="antialiased bg-gradient-to-br from-green-100 to-white">
	    <div class="container px-6 mx-auto">
	      <div
	        class="flex flex-col text-center md:text-left md:flex-row h-screen justify-evenly md:items-center"
	      >
	        <div class="flex flex-col w-full">
	          <div>
	            <svg
	              class="w-20 h-20 mx-auto md:float-left fill-stroke text-gray-800"
	              fill="none"
	              stroke="currentColor"
	              viewBox="0 0 24 24"
	              xmlns="http://www.w3.org/2000/svg"
	            >
	              <path
	                stroke-linecap="round"
	                stroke-linejoin="round"
	                stroke-width="2"
	                d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
	              ></path>
	            </svg>
	          </div>
	          <h1 class="text-5xl text-gray-800 font-bold">Client Area</h1>
	          <p class="w-5/12 mx-auto md:mx-0 text-gray-500">
	            Activate your account by clicking on activate button.
	          </p>
	        </div>
	        <div class="w-full md:w-full lg:w-9/12 mx-auto md:mx-0">
	          <div class="bg-white p-10 flex flex-col w-full shadow-xl rounded-xl">
	            <h2 class="text-2xl font-bold text-gray-800 text-left mb-5">
	              Activation
	            </h2>
	            <form action="" class="w-full">
	              <div id="input" class="flex flex-col w-full my-5">
	                <label for="username" class="text-gray-500 mb-2"
	                  >Username</label
	                >
	                <input
	                  type="text"
	                  v-model="username"
	                  id="username"
	                  placeholder="Please insert your username"
	                  class="appearance-none border-2 border-gray-100 rounded-lg px-4 py-3 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-green-600 focus:shadow-lg"
	                />
	              </div>
	              <div id="input" class="flex flex-col w-full my-5">
	                <label for="username" class="text-gray-500 mb-2"
	                  >Email</label
	                >
	                <input
	                  type="text"
	                  v-model="email"
	                  id="email"
	                  placeholder="Please insert your email"
	                  class="appearance-none border-2 border-gray-100 rounded-lg px-4 py-3 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-green-600 focus:shadow-lg"
	                />
	              </div>
	              <div id="input" class="flex flex-col w-full my-5">
	                <label for="username" class="text-gray-500 mb-2"
	                  >Token</label
	                >
	                <input
	                  type="text"
	                  v-model="token"
	                  id="first_name"
	                  placeholder="Please insert your first name"
	                  class="appearance-none border-2 border-gray-100 rounded-lg px-4 py-3 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-green-600 focus:shadow-lg"
	                />
	              </div>
	              <div id="button" class="flex flex-col w-full my-5">
	                <button
	                  type="button"
	                  class="w-full py-4 bg-green-600 rounded-lg text-green-100"
	                >
	                  <div @click="activationHandler()" class="flex flex-row items-center justify-center">
	                    <div class="mr-2">
	                      <svg
	                        class="w-6 h-6"
	                        fill="none"
	                        stroke="currentColor"
	                        viewBox="0 0 24 24"
	                        xmlns="http://www.w3.org/2000/svg"
	                      >
	                        <path
	                          stroke-linecap="round"
	                          stroke-linejoin="round"
	                          stroke-width="2"
	                          d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
	                        ></path>
	                      </svg>
	                    </div>
	                    <div class="font-bold">Activate</div>
	                  </div>
	                </button>
	              </div>
	            </form>
	          </div>
	        </div>
	      </div>
	    </div>
	</div>
</template>
<script type="text/javascript">
	import { mapFields } from "vuex-map-fields";
	import { map } from "lodash";
	export default {
	   data() {
	      return {
	         username: this.$route.query.username,
	         email: this.$route.query.email,
	         token: this.$route.query.token,
	      };
	   },
	   methods: {
	      activationHandler() {
		      const data = {
		         username: this.username,
		         email: this.email,
		         token: this.token,
		      }
	      	this.$store.dispatch("auth/StartActivation", data);
	      },
	    },
	};
// export default {
//    name: "Signup",
//    data() {
//       return {
//          username: this.$route.query.username,
//          email: this.$route.query.email,
//          token: this.$route.query.token,
//       };
//    },

//    methods: {
//       async activationHandler() {
//          const data = {
//             username: this.username,
//             email: this.email,
//             token: this.token,
//          };
//          try {
//             const res = await this.$axios.post("http://10.10.6.87/pmp/api/user/activate/", data)
//             console.log(res.data.message)
//          } catch (e) {
//             console.log(e.response.data.message)
//          }
//       },
//    },
// };
</script>