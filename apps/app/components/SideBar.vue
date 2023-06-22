<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "SideBar"
})
</script>

<template>
  <div id="container">
    <div>Home</div>
    <div>
      Config Variant Option
    </div>
    <div>Design Library</div>
    <div>Activate App on Themes</div>
  </div>
</template>

<style scoped>
#container {
  display: flex;
  overflow: auto;
  flex: auto;
  flex-direction: column;
  align-items: stretch;
  max-width: 300px;
  gap: 50px;
}
</style>