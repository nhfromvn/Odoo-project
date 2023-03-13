<template>
  <div id="container">
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
}

#frame_50 {
  height: 34px;
  width: 133px;
  left: 1282px;
  border-radius: 0px;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  padding: 0px;
  gap: 26px;
  position: relative;
  right: 25px;
  top: calc(50% - 34px / 2 - 0.5px);

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
  left: 49px;
  top: 5px;
  border-radius: 0px;
  /* Inside auto layout */
  flex: none;
  order: 1;
  flex-grow: 0;
}

#elip_102 {
  height: 6px;
  width: 6px;
  left: 15px;
  top: 2px;
  background: #DB3737;
  border-radius: 50%;
  position: relative;

}

#icon {
  height: 20px;
  width: 17.478065490722656px;
  left: 3.2607421875px;
  top: 2px;
  position: relative;

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