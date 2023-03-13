<template>
  <head>
<!--    <link rel="stylesheet" href="/bought_together/static/css/style.css">-->
  </head>
  <div id="container">
    <div id="frame_427318695">
      <div class="elip" id="elip_103">
      </div>
      <div id="nest_scale">
        NestScale
      </div>
    </div>
    <div id="frame_427318741">
      <div class="elip" id="elip_28">
      </div>
    </div>
    <div class="elip" id="elip_28">
    </div>
    <div class="elip" id="elip_28">
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
  position: absolute;
  background: #EFEFEF;
}

#frame_427318695 {
  /* Auto layout */
  height: 46px;
  width: 181px;
  left: 20px;
  top: 24px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;
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

#nest_scale {
  width: 123px;
  height: 24px;
  left: 58px;
  top: 11px;
  font-family: 'Open Sans', sans-serif, 'Kanit';
  font-style: normal;
  font-weight: 600;
  font-size: 27px;
  line-height: 24px;
  /* identical to box height, or 89% */
  color: #17181A;
  /* Inside auto layout */
  flex: none;
  order: 1;
  flex-grow: 0;
}

#elip_103 {
  width: 46px;
  height: 46px;
  background: #000000;
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