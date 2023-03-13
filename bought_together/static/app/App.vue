<template>
  <SlideBar/>
  <NavBar/>

</template>

<script>

import SlideBar from "./components/SlideBar.vue";
import NavBar from "./components/NavBar.vue";

export default {
    name: "App",
    components:{
      NavBar,
      SlideBar


    },
    data() {
          return {



          }
      },
  methods:{

  },
    mounted() {
      console.log("Hello shopify")

    }

}

</script>
<style>
#app{


}

body{

}
</style>