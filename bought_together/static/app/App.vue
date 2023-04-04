<template>
  <NavBar/>
  <div style="display: flex;">
    <SlideBar :is_selected="is_selected" @CustomEventChanged="get_select_id"/>
    <Loading v-if="!products"/>
    <Dashboard :proptemp="temp" v-if="is_selected=='dashboard'"/>
    <AddProduct :list_products="products" v-if="is_selected=='add_product'" @send_lists="get_lists"
                @goTo="go"/>
    <Customization
        :proptemp="temp"
        @saveCustomization="get_customize" @goTo="go" v-if="is_selected=='customization'"/>
    <Installation :shop_url="shop_url" @goTo="go" v-if="is_selected=='installation'"/>
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
      this.temp.list_recommend_product = data.list_recommend
      this.temp.list_exclude_product = data.list_exlcude
      this.is_selected = 'customization'
      this.check = data.check
    },
    get_customize(data) {
      this.widget_title = data.widget_title
      this.widget_title_color = data.widget_title_color
      this.widget_title_font_size = data.widget_title_font_size
      this.widget_description = data.widget_description
      this.widget_description_color = data.widget_description_color
      this.widget_description_font_size = data.widget_description_font_size
      this.widget_button_text = data.widget_button_text
      this.widget_button_text_color = data.widget_button_text_color
      this.widget_button_bg_color = data.widget_button_bg_color
      this.widget_button_border_color = data.widget_button_border_color
      this.product_included = data.product_included
      this.total_price = data.total_price
      this.is_selected = 'dashboard'
      let params = {
        widget_title: data.widget_title,
        widget_title_color: data.widget_title_color,
        widget_title_font_size: data.widget_title_font_size,
        widget_description: data.widget_description,
        widget_description_color: data.widget_description_color,
        widget_description_font_size: data.widget_description_font_size,
        widget_button_text: data.widget_button_text,
        widget_button_text_color: data.widget_button_text_color,
        widget_button_bg_color: data.widget_button_bg_color,
        widget_button_border_color: data.widget_button_border_color,
        product_included: data.product_included,
        total_price: data.total_price,
        list_recommend_product: this.list_recommend_product,
        list_exclude_product: this.list_exclude_product
      }
      axios.post('/bought-together/save/product', params).then((res) => {
        if (res.data.result.status) {
          alert('Save Success')
        }
      })
    }
  },
  mounted() {
    let self = this
    axios.get("/bought-together/sync/product").then((res) => {
      self.products = res.data.products
      self.shop_url = res.data.shop_url
      for (let product of self.products) {
        product.check_recommend = self.list_recommend_product_id.includes(String(product.product_id));
        product.check_exclude = self.list_exclude_product_id.includes(String(product.product_id));
      }
    })
    axios.get("/bought-together/get/widget").then((res) => {
      self.list_recommend_product_id = res.data.list_recommend_product
      self.list_exclude_product_id = res.data.list_exclude_product
      self.temp.widget_title = res.data.widget_title
      self.temp.widget_title_color = res.data.widget_title_color
      self.temp.widget_title_font_size = res.data.widget_title_font_size
      self.temp.widget_description = res.data.widget_description
      self.temp.widget_description_color = res.data.widget_description_color
      self.temp.widget_description_font_size = res.data.widget_title_font_size
      self.temp.widget_button_text = res.data.widget_button_text
      self.temp.widget_button_text_color = res.data.widget_button_text_color
      self.temp.widget_button_bg_color = res.data.widget_button_bg_color
      self.temp.widget_button_border_color = res.data.widget_button_border_color
      self.temp.product_included = res.data.product_included
      self.temp.total_price = res.data.total_price
    })

  },
  data() {
    return {
      is_selected: 'dashboard',
      products: [],
      shop_url: '',
      list_recommend_product_id: [],
      list_exclude_product_id: [],
      temp: {
         font_sizes: [{
        name: 'Extra Small', value: 12
      }, {
        name: 'Small', value: 16
      }, {
        name: 'Medium', value: 18
      }, {
        name: 'Large', value: 20
      }, {
        name: 'Extra Large', value: 25
      }],
        list_exclude_product: [],
        list_recommend_product: [],
        widget_title: '',
        widget_title_color: '',
        widget_title_font_size: '',
        widget_description: '',
        widget_description_color: '',
        widget_description_font_size: '',
        widget_button_text: '',
        widget_button_text_color: '',
        widget_button_bg_color: '',
        widget_button_border_color: '',
        product_included: 0,
        total_price: 0
      }
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