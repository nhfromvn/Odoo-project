<template>
  <div id="container">

    <div style="display: flex;
                                     gap:5px">

      <div v-if="is_selected_copy==pages[0]" class="frame_427318741 is_select">
        <p>
          Home</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(0)">
        <p>
          Home </p>
      </div>
    </div>

    <div style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[1]" class="frame_427318741 is_select">
        <p>
          Activate app</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(1)">
        <p>
          Activate app</p>
      </div>
    </div>

    <div style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[2]" class="frame_427318741 is_select">
        <p>
          Config variant option</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(2)">
        <p>
          Config variant option</p>
      </div>
    </div>
    <div style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[3]" class="frame_427318741 is_select">
        <p>
          Customize Style</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(3)">
        <p>
          Customize Style</p>
      </div>
    </div>
  </div>
</template>
<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "SideBar",
  data() {
    return {
      pages: ['home', 'activate_app', 'config_variant_option', 'customize_style'],
    }
  },
  methods: {
    onClick(id) {
      this.is_selected_copy = this.pages[id]
      this.$emit('CustomEventChanged', this.pages[id])
    },
  },
  computed: {
    is_selected_copy: function () {
      return this.is_selected
    }
  }
})
</script>
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

#container {
  height: 100%;
  width: auto;
  position: fixed;
  padding: 24px 20px 0px 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 32px;
  background: #EFEFEF;
}

.frame_427318741 {
  height: 32px;
  width: 204px;
  text-align: center;
  background: #EFEFEF;
  display: flex;
  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;
}

.frame_427318741 p {
  padding: 2.5%;

}

.is_select {
  background-color: #ffffff !important;
}
</style>