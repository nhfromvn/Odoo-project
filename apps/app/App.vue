<template>
  <div style="display: flex">
    <SideBar :is_selected="is_selected" @CustomEventChanged="get_select_id"/>
    <div class="container">
      <Home v-if="is_selected=='home'"/>
      <ActivateApp v-if="is_selected=='activate_app'" :proptemp="activate_app_temp" @saveData="saveTheme"/>
      <ConfigVariantOption :proptemp="config_variant_temp" @saveData="saveDataConfigVariant"
                           v-if="is_selected=='config_variant_option'"/>
      <CustomizeStyle :proptemp="customize_temp" @saveData="savePoductStyle"
                      v-if="is_selected=='customize_style'"/>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SideBar from "./components/SideBar.vue";
import ConfigVariantOption from "./components/ConfigVariantOption.vue";
import Home from "./components/Home.vue";
import ActivateApp from "./components/ActivateApp.vue";
import CustomizeStyle from "./components/CustomizeStyle.vue";

export default {
  data() {
    return {
      is_selected: 'home',
      server_data: null,
      config_variant_temp: {
        options: [],
        general: {},
        styles:[],
      },
      activate_app_temp: {},
      customize_temp: [],
    }
  },
  components: {
    CustomizeStyle,
    ActivateApp,
    Home,
    ConfigVariantOption,
    SideBar
  },
  computed: {},
  methods: {
    get_select_id(data) {
      this.is_selected = data
    },
    saveDataConfigVariant(param) {
      console.log(param)
      axios.post('/king_variant/save/option_data', param).then((res) => {
        console.log(res)
        if (res.data.result) {
          alert('save success')
        } else {
          alert('error')
        }
      })
    },
    saveTheme(param) {
      console.log(param)
      axios.post('/king_variant/save/theme', {themes: param}).then((res) => {
        console.log(res)
        if (res.data.result) {
          alert('change status success')
        } else {
          alert('error')
        }
      })
    }
  },
  mounted() {
    let self = this
    axios.get('/king_variant/get_product').then((res) => {
      console.log(res)
      axios.get('/king_variant/get_data').then((res) => {
        console.log(res)
        self.server_data = res.data
        self.config_variant_temp.options = res.data.options
        self.config_variant_temp.general = res.data.general
        self.config_variant_temp.styles = res.data.styles
        self.activate_app_temp = res.data.theme
        self.customize_temp = res.data.styles
        console.log(self.config_variant_temp)
        console.log(self.server_data)
        console.log(self.activate_app_temp)

      })
    })

  }
}
</script>
<style>
.container {
  display: block;
  width: 100%;
  margin: 83px 80px 100px 300px;
}
</style>


