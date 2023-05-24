<template>
  <div id="container">
    <div id="dashboard" style="display: flex;
                                     gap:5px">

      <div v-if="is_selected_copy==pages[0]" class="frame_427318741 is_select">
        <p>
          Dashboard</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(0)">
        <p>
          Dashboard</p>
      </div>
    </div>

    <div id="integration" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[1]" class="frame_427318741 is_select">
        <p>
          Integration</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(1)">
        <p>
          Integration</p>
      </div>
    </div>

    <div id="meida_source" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[2]" class="frame_427318741 is_select">
        <p>
          Media Source</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(2)">
        <p>
          Media Source</p>
      </div>
    </div>
    <div id="widgets" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[3]" class="frame_427318741 is_select">
        <p>
          Widgets</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(3)">
        <p>
          Widgets</p>
      </div>
    </div>
  </div>
</template>
<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "SideBar",
  props: {is_selected: String},
  data() {
    return {
      pages: ['dashboard', 'integration', 'media_source', 'widget'],
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
</style>