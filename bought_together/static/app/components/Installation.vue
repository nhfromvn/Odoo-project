<template>
  <div class="container" id="container">
    <div class="d-flex justify-content-center">
      <div id="frame_427319039">
        <button class="head_btn" id="add_product">Add Product</button>
        <button class="head_btn" id="customization">Customization</button>
        <button class="head_btn" id="installation">Installation</button>
      </div>
    </div>
    <div class="d-flex justify-content-end">
      <div class="right_top_btns" style="display: flex; gap: 19px">
        <button id="btn_home">
          Home
        </button>
        <button id="btn_go_to_customize">
          Go To Customization
        </button>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <p id="congratulation">CONGRATULATION! YOU HAVE CREATED WIDGET SUCCESSFULLY! </p>
    </div>
    <div class="d-flex justify-content-center">
      <p id="instruction">Now please follow these steps below to display it on your product pages </p>
    </div>
    <div class="d-flex justify-content-center">
      <p class="lorem_ipsum">
        <br/>1. Lorem ipsum is placeholder text commonly used in the graphic, print
        <br/>2. and publishing industries for previewing layouts and visual mockups.
        <br/>3. Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for
        previewing
        layouts and visual mockups.
      </p>
    </div>
    <div class="d-flex justify-content-center">
      <div class="d-flex justify-content-center align-items-center" id="rectangle_34624157">
         <video controls height="85%" width="85%">
            <source src="/bought_together/static/app/video/cuu-non-120739.mp4" type="video/mp4">
        </video>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Installation"
}
</script>

<style scoped>
#installation {
  box-sizing: border-box;

  /* Auto layout */

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 6px 16px;
  width: 184.67px;
  height: 36px;
  background: #FFFFFF;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.25);
}

#btn_home {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-size: 14px;
  line-height: 24px;
  height: 32px;
  border-radius: 4px;
  padding: 4px 12px 4px 12px;
  background: #E2E2E2;
  display: flex;
  flex-direction: row;
  align-items: center;
}

#btn_go_to_customize {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-size: 14px;
  line-height: 24px;
  text-align: center;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 4px 12px;
  gap: 4px;
  height: 32px;
  color: #FFFFFF;
  background: #1D1E21;
  border-radius: 4px;
}

#congratulation {
  width: 697px;
  height: 24px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 22px;
  /* or 110% */
  text-align: center;
  color: #000000;
  margin: 5px;
}

#instruction {
  width: 493px;
  height: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 22px;
  /* identical to box height, or 157% */
  color: #000000;
}

.lorem_ipsum {
  width: 752px;
  height: 110px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 22px;
  text-align: left;
}

#rectangle_34624157 {


}

</style>