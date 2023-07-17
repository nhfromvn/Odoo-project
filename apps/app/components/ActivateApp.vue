<template>
  <h2>Themes</h2>
  <div v-for="theme in proptemp" class="theme_line">
    <div style="display:flex;"><h2 style="margin: 0">{{ theme.theme_name }}</h2>
      <p>({{ theme.role }})</p></div>
    <input style="margin: 0px 10px 0px 0px" type="checkbox" @change="save" v-model="theme.is_active"/>
  </div>
</template>
<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "ActivateApp",
  props: {
    proptemp: Object
  },
  methods: {
    save() {
      this.$emit('saveData', this.proptemp)
    }
  }
})
</script>


<style scoped>

</style>