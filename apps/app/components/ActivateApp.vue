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
.theme_line {
  display: flex;
  justify-content: space-between;
  padding: 2rem 2rem;
  align-items: center;
  width: 100%;
  cursor: pointer;
  appearance: none;
  margin: 0;
  background: #d5d5d5;
  border: none;
  font-size: inherit;
  line-height: inherit;
  color: inherit;
  text-align: left;
  position: relative;
  border-radius: 10px;
}
</style>