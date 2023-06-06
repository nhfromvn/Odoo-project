<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DashBoard",
  props: {
    proptemp: Object
  },
  mounted() {
    console.log(this.proptemp.app_user)
  }
})
</script>

<template>

  <div v-if="proptemp.shop_url">
    <div v-if="proptemp.app_user">
      Hello, {{ proptemp.app_user }}
    </div>
    <div v-else>
      Hello, {{ proptemp.shop_url }}
    </div>
  </div>
  <div v-else>
    Your account is not connected to any store yet
    <br>
    Click <a href="https://admin.shopify.com/">here</a> to connect
  </div>
  <div>
    Guide
  </div>

</template>

<style scoped>

</style>