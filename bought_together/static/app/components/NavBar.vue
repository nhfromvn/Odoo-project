<template>
  <div id="container">
    <div style="display: flex" id="frame_427318695">
      <img class="elip" id="elip_103" src="/bought_together/static/app/img/nest_scale.jpeg">
      <div id="nest_scale">
        NestScale
      </div>
    </div>
    <div id="frame_50">
      <div id="question-mark_major">
        <img id="primary_fill" src="/bought_together/static/app/img/img_1.png">
      </div>
      <div id="bell_01">
        <div id="elip_102">
        </div>
        <img id="icon" src="/bought_together/static/app/img/img.png">
      </div>
      <img id="elip_101" src="/bought_together/static/app/img/img_2.png">
    </div>
  </div>
</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style scoped>
#container {
  height: 83px;
  width: 100%;
  background: #EFEFEF;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px 20px;
}

#frame_50 {
  height: 34px;
  width: 133px;
  border-radius: 0px;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  padding: 0px;
  gap: 26px;
}

#frame_427318695 {
  /* Auto layout */
  height: 46px;
  width: 181px;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  /* Inside auto layout */
  flex: none;
  order: 0;
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

#question-mark_major {
  height: 23px;
  width: 23px;
  left: 0px;
  top: 5.5px;
  border-radius: 0px;
  flex: none;
  order: 0;
  flex-grow: 0;

}

#primary_fill {
  height: 23px;
  width: 23px;
  left: 0px;
  top: 0px;
  border-radius: 0px;
}

#bell_01 {
  height: 24px;
  width: 24px;
  border-radius: 0px;
  /* Inside auto layout */
  flex: none;
  order: 1;
  flex-grow: 0;
  position: relative;
}

#elip_102 {
  height: 6px;
  width: 6px;
  right: 5px;
  background: #DB3737;
  border-radius: 50%;
  position: absolute;
}

#icon {
  height: 20px;
  width: 17.478065490722656px;
  left: 3.2607421875px;
}

#elip_101 {
  height: 34px;
  width: 34px;
  left: 99px;
  top: 0px;
  border-radius: 50%;
  flex: none;
  order: 2;
  flex-grow: 0;

}
</style>