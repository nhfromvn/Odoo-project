<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar @CustomEventChanged="get_select_id"/>
    <Dashboard v-if="is_selected=='dashboard'"/>
    <AddProduct :list_products="products" v-if="is_selected=='add_product'"/>
    <Customization v-if="is_selected=='customization'"/>
    <Installation v-if="is_selected=='installation'"/>
    <Loading v-if="is_selected==''"/>
  </div>

</template>

<script>
import axios from 'axios'
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

  methods: {
    get_select_id(data) {
      this.is_selected = data;
    }
  },
  mounted() {
    let self = this
    axios.get("/bought-together/sync/product").then((res) => {
      self.products = res.data.products
      self.shop_url = res.data.shop_url
      console.log(self.products)
      for (let product of self.products) {
        product.check_recommend = false
        product.check_exclude = false
      }
    })
  },
  data() {
    return {
      is_selected: '',
      products: [],
      shop_url: '',
      list_recommend_product:[],
      list_exclude_product:[],
    }
  },
}

</script>
<style>
#app {


}

NavBar {
  z-index: 0;
}

SlideBar {
  z-index: 1;
}

Content {
  z-index: 2;
}
</style>