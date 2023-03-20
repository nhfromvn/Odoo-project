<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar/>
    <Content/>
  </div>
</template>

<script>

import SlideBar from "./components/SlideBar.vue";
import NavBar from "./components/NavBar.vue";
import Content from "./components/Content.vue";

export default {
  name: "App",
  components: {
    Content,
    NavBar,
    SlideBar
  },
  data() {
    return {}
  },
  methods: {},
  mounted() {
    console.log("Hello shopify")

  }

}

</script>
<style>
#app {


}

SlideBar {
  z-index: 1;
}

Content {
  z-index: 2;
}
</style>