<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CustomizeStyle",
  props: {
    proptemp: Object
  }
})
</script>

<template>
  <h2>Customize style for variant option</h2>
  <div v-for="style in proptemp">
    {{style}}
  </div>
</template>

<style scoped>

</style>