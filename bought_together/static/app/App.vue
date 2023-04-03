<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar :is_selected="is_selected" @CustomEventChanged="get_select_id"/>
    <Dashboard :widget_title="widget_title" :widget_description="widget_description"
               :product_included="product_included" :total_price="total_price" v-if="is_selected=='dashboard'"/>
    <AddProduct :list_products="products" v-if="is_selected=='add_product'" @send_lists="get_lists" @goTo="go"/>
    <Customization :list_recommend_product="list_recommend_product" :list_exclude_product="list_exclude_product"
                   @saveCustomization="get_customize" @goTo="go" v-if="is_selected=='customization'"/>
    <Installation :shop_url="shop_url" @goTo="go" v-if="is_selected=='installation'"/>
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
    go(data) {
      this.is_selected = data;
    },
    get_select_id(data) {
      this.is_selected = data;
    },
    get_lists(data) {
      this.list_recommend_product = data.list_recommend
      this.list_exclude_product = data.list_exlcude
      this.is_selected = 'customization'
      this.check = data.check
    },
    get_customize(data) {
      this.widget_title = data.widget_title
      this.widget_description = data.widget_description
      this.product_included = data.product_included
      this.total_price = data.total_price
      console.log(this)
      this.is_selected = 'dashboard'
    }
  },
  mounted() {
    let self = this
    axios.get("/bought-together/sync/product").then((res) => {
      self.products = res.data.products
      self.shop_url = res.data.shop_url
      for (let product of self.products) {
        product.check_recommend = false
        product.check_exclude = false
      }
    })
  },
  data() {
    return {
      is_selected: 'dashboard',
      products: [],
      shop_url: '',
      list_recommend_product: [],
      list_exclude_product: [],
      widget_title: 'sdfsd',
      widget_description: 'dsd',
      product_included: 3,
      total_price: 4,
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