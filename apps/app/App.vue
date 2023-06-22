<template>
  <div style="display: flex">
    <SideBar/>
    <div class="container">
      <ConfigVariantOption/>
    </div>
  </div>
  <button @click="onClick">Click me</button>
  <div>
    <button @click="onClick2">Click me</button>
  </div>

</template>

<script>
import axios from 'axios'
import SideBar from "./components/SideBar.vue";
import ConfigVariantOption from "./components/ConfigVariantOption.vue";

export default {
  data() {
    return {}
  },
  components: {ConfigVariantOption, SideBar},
  computed: {},
  methods: {
    onClick() {
      axios.get('/king_variant/get_product').then((res) => {
        console.log(res)
      })
    },
    onClick2() {
      axios.get('/king_variant/get_data').then((res) => {
        console.log(res)
      })
    }
  },
  mounted() {


  }
}
</script>
<style>

</style>


