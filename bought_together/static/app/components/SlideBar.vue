<template>
  <div id="container">
    <div id="frame_427318741">
      <div class="elip" id="elip_28">
      </div>
    </div>
    <div id="frame_427318741">
      <div class="elip" id="elip_28"/>
    </div>
    <div id="frame_427318741">
      <div class="elip" id="elip_28"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "SlideBar"
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

#frame_427318741 {
  height: 32px;
  width: 236px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
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