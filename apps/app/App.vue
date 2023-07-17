<template>
  <div style="display: flex">
    <SideBar :is_selected="is_selected" @CustomEventChanged="get_select_id"/>
    <div class="container">
      <Home v-if="is_selected=='home'"/>
      <ActivateApp v-if="is_selected=='activate_app'" :proptemp="activate_app_temp" @saveData="saveTheme"/>
      <ConfigVariantOption :proptemp="config_variant_temp" @saveData="saveDataConfigVariant"
                           v-if="is_selected=='config_variant_option'"/>
      <CustomizeStyle :proptemp="customize_temp" @saveStyle="savePoductStyle"
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
        styles: [],
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
    savePoductStyle(param) {
      axios.post('/king_variant/save/style', {params: param, jsonrpc: '2.0'}).then((res) => {
        console.log(res)
        if (res.data.result) {
          alert('Save success')
        } else {
          alert('error')
        }
      })
    },
    get_select_id(data) {
      this.is_selected = data
    },
    saveDataConfigVariant(param) {
      console.log(param)
      axios.post('/king_variant/save/option_data', {params: param, jsonrpc: '2.0'}).then((res) => {
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
      axios.post('/king_variant/save/theme', {
        jsonrpc: '2.0',
        params: {
          themes: param
        }
      }).then((res) => {
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
    axios.post('/king_variant/get_product', {
      jsonrpc: '2.0',
      params: {
        store_url: window.location,
      }
    }).then((res) => {
      console.log(res)
      axios.post('/king_variant/get_data', {
        jsonrpc: '2.0',
        params: {
          store_url: window.location,
        }
      }).then((res) => {
        console.log(res)
        self.server_data = res.data.result
        self.config_variant_temp.options = res.data.result.options
        self.config_variant_temp.general = res.data.result.general
        self.config_variant_temp.styles = res.data.result.styles
        self.activate_app_temp = res.data.result.theme
        self.customize_temp = res.data.result.styles
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


