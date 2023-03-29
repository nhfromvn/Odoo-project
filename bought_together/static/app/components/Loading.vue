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
        <button class="is_loading">
        </button>
        <button class="is_loading">
        </button>
      </div>
    </div>
    <div id="rectangle_1"/>
    <div id="rectangle_1"/>
    <div id="rectangle_2" class="is_loading"/>
    <div id="rectangle_2" class="is_loading"/>

  </div>
</template>

<script>
export default {
  name: "Loading"
}
</script>

<style scoped>
#add_product{
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
.right_top_btns {
  margin-bottom: 0px;
  width: 200px;
}

.right_top_btns button {
  height: 32px;
  width: 80px;
  border-radius: 4px;
  padding: 4px 12px 4px 12px;
  background: #E2E2E2;
  display: flex;
  flex-direction: row;
  align-items: center;
}

#rectangle_1 {
  width: 246px;
  height: 22px;
  background: #F2F2F2;
  border-radius: 3px;
  margin: 10px 0px;
}

#rectangle_2 {
  height: 317px;
  width: 100%;
  margin: 17px 0px;
}
</style>