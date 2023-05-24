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
  <div>
    Hello,{{proptemp.app_user}}
  </div>
</template>

<style scoped>

</style>