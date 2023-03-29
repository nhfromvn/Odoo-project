<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar @CustomEventChanged="get_select_id"/>
    <Dashboard v-if="is_selected=='dashboard'"/>
    <AddProduct v-if="is_selected=='add_product'"/>
    <Customization v-if="is_selected=='customization'"/>
    <Installation v-if="is_selected=='installation'"/>
    <Loading v-if="is_selected==''"/>
  </div>

</template>

<script>
import SlideBar from "./components/SlideBar.vue";
import NavBar from "./components/NavBar.vue";
import Dashboard from "./components/Dashboard.vue";
import AddProduct from "./components/AddProduct.vue";
import Customization from "./components/Customization.vue";
import Installation from "./components/Installation.vue";
import Loading from "./components/Loading.vue";

export default {
  name: "App",
  components: {
    Loading,
    Installation,
    Customization,
    AddProduct,
    Dashboard,
    NavBar,
    SlideBar
  },
  data() {
    return {
      is_selected: ''
    }
  },
  methods: {
    get_select_id(data) {
      this.is_selected = data;
    }
  },
  mounted() {
  }

}

</script>
<style>
#app {


}
NavBar{
  z-index: 0;
}
SlideBar {
  z-index: 1;
}

Content {
  z-index: 2;
}
</style>