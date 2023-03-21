<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar @CustomEventChanged="get_select_id"/>
    <Dashboard v-if="is_selected=='dashboard'"/>
    <AddProduct v-if="is_selected=='add_product'"/>
    <Customization v-if="is_selected=='customization'"/>
    <Installation v-if="is_selected=='installation'"/>
  </div>

</template>

<script>

import SlideBar from "./components/SlideBar.vue";
import NavBar from "./components/NavBar.vue";
import Dashboard from "./components/Dashboard.vue";
import AddProduct from "./components/AddProduct.vue";
import Customization from "./components/Customization.vue";
import Installation from "./components/Installation.vue";

export default {
  name: "App",
  components: {
    Installation,
    Customization,
    AddProduct,
    Dashboard,
    NavBar,
    SlideBar
  },
  data() {
    return {
      is_selected: 'dashboard'
    }
  },
  methods: {
    test() {
      console.log(SlideBar.data().is_selected)
    },
    get_select_id(data) {
      this.is_selected = data;
      console.log(data)
    }
  },

  mounted() {
    this.test()
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