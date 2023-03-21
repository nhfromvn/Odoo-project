<template>
  <div id="container">
    <div id="dashboard" style="display: flex;
                                     gap:5px">
      <div class="elip" id="elip_28">
      </div>
      <div class="frame_427318741 is_select">
        Dashboard
      </div>
    </div>

    <div id="add_product" style="display: flex;
                                     gap:5px">
      <div class="elip" id="elip_28">
      </div>
      <div class="frame_427318741">
        Add Product
      </div>
    </div>

    <div id="customization" style="display: flex;
                                     gap:5px">
      <div class="elip" id="elip_28">
      </div>
      <div class="frame_427318741">
        Customization
      </div>
    </div>
    <div id="installation" style="display: flex;
                                     gap:5px">
      <div class="elip" id="elip_28">
      </div>
      <div class="frame_427318741">
        Installation
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SlideBar",
  data() {
    return {
      is_selected:'',
      test: 'hello'
    }
  }

}
</script>
<style scoped>
#container {
  height: 1024px;
  width: 276px;
  padding: 24px 20px 0px 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 32px;
  background: #EFEFEF;
}

.frame_427318741 {
  height: 32px;
  width: 180px;
  text-align: center;
  background: #FFFFFF;
  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;
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