<template>
  <div id="container">
    <div id="dashboard" style="display: flex;
                                     gap:5px">

      <div v-if="is_selected_copy==pages[0]" class="frame_427318741 is_select">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Dashboard</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(0)">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Dashboard</p>
      </div>
    </div>

    <div id="add_product" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[1]" class="frame_427318741 is_select">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Add Product</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(1)">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Add Product</p>
      </div>
    </div>

    <div id="customization" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[2]" class="frame_427318741 is_select">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Customization</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(2)">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Customization</p>
      </div>
    </div>
    <div id="installation" style="display: flex;
                                     gap:5px">
      <div v-if="is_selected_copy==pages[3]" class="frame_427318741 is_select">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Installation</p>
      </div>
      <div v-else class="frame_427318741" @click="onClick(3)">
        <div class="elip" id="elip_28">
        </div>
        <p>
          Installation</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SlideBar",
  props: {is_selected: String},
  data() {
    return {
      pages: ['dashboard', 'add_product', 'customization', 'installation'],
    }
  },
  methods: {
    onClick(id) {
      this.is_selected_copy = this.pages[id]
      this.$emit('CustomEventChanged',this.pages[id])
    },
  },
  computed:{
    is_selected_copy: function(){
      return this.is_selected
    }
  }

}
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
  top: 83px;
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

#elip_28 {
  width: 32px;
  height: 32px;
  background: #D9D9D9;
  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;
}
</style>