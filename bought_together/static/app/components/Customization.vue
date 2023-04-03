<template>
  <div class="container" id="container">
    <div class="d-flex justify-content-center">
      <div id="frame_427319039">
        <button class="head_btn" id="add_product">Add Product</button>
        <button class="head_btn is_select" id="customization">Customization</button>
        <button class="head_btn" id="installation">Installation</button>
      </div>
    </div>
    <div class="d-flex justify-content-end">
      <div class="right_top_btns" style="display: flex; gap: 19px">
        <button id="btn_cancel">
          Cancel
        </button>
        <button id="btn_save">
          SAVE
        </button>
      </div>
    </div>
    <div style="display: flex; gap:100px">
      <div id="content_left">
        <div id="text_settings" class="d-flex align-items-center">
          <p>Settings</p>
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
        </div>
        <div id="text_general_configuration" class="d-flex align-items-center ">
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>General Configuration</p>
        </div>
        <div id="widget_title">
          <p>Widget Title</p>
          <input type="text" v-model="widget_title" @input="updateWidgetTitle()">
        </div>
        <div id="title_color_and_font-size">
          <div id="title_color">
            <p>Title Color</p>
            <div class="d-flex align-items-center">
              <div class="color_input">
                <input type="color" v-model="title_color">
              </div>
              <input type="text" v-model="title_color">
            </div>
          </div>
          <div id="title_font_size"><p>Title Font Size</p>
            <select v-model="title_font_size">
              <option class="option_style" v-for="option in font_sizes" :value="option">{{ option }}</option>
            </select></div>
        </div>
        <div id="widget_description">
          <p>Widget Description</p>
          <input type="text" v-model="widget_descciption" @input="updateWidgetDescription()">
        </div>
        <div id="description_color_and_font-size" style="display: flex">
          <div id="description_color">
            <p>Description Color</p>
            <div class="d-flex">
              <div class="d-flex align-items-center">
                <div class="color_input">
                  <input type="color" v-model="description_color">
                </div>
                <input type="text" v-model="description_color">
              </div>
            </div>
          </div>
          <div id="description_font_size">
            <p>Description Font Size</p>
            <select v-model="description_font_size">
              <option class="option_style" v-for="option in font_sizes" :value="option">{{ option }}</option>
            </select></div>
        </div>
        <div id="layout_and_number" style="display: flex">
          <div id="layout_style">
            <p>Layout Style</p>
          </div>
          <div id="number_of_product">
            <p>Number of products to show</p>
            <input type="number" value="3" min="1" max="5">
          </div>
        </div>
        <div id="text_button_configuration" class="d-flex align-items-center">
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>Button Configuration</p>
        </div>
        <div id="button_text">
          <p>
            Button Text
          </p>
          <input type="text" v-model="button_text" @input="updateButtonText()">
        </div>
        <div id="button_text_color">
          <p>
            Button Text Color
          </p>
          <div class="d-flex align-items-center">
            <div class="color_input">
              <input type="color" v-model="btn_text_color">
            </div>
            <input type="text" v-model="btn_text_color">
          </div>

        </div>
        <div style="display: flex; justify-content: space-between; padding-bottom: 30px">
          <div id="button_bg_color">
            <p>
              Button Background Color
            </p>
            <div class="d-flex align-items-center">
              <div class="color_input">
                <input type="color" v-model="btn_bg_color">
              </div>
              <input type="text" v-model="btn_bg_color">
            </div>
          </div>
          <div id="button_border_color">
            <p>
              Button Border Color
            </p>
            <div class="d-flex align-items-center">
              <div class="color_input">
                <input type="color" v-model="btn_border_color">
              </div>
              <input type="text" v-model="btn_border_color">
            </div>
          </div>

        </div>
        <div id="content_right"></div>

      </div>
      <div id="content_right" class="d-flex align-items-center">
        <div id="text_preview">
           <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>Preview</p>
        </div>
        <div id="rectangle_preview">
          <div>{{ widget_title }}</div>
          <div>{{ widget_descciption }}</div>
          <div style="display: flex">
            <div>product</div>
            <div>
              <div>Total:</div>
              <div>
                <button>
                  {{ button_text }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Customization",
  data() {
    return {
      btn_text_color: '#FFFFF',
      btn_bg_color: '#FFFFF',
      btn_border_color: '#FFFFF',
      description_color: '#FFFFF',
      title_color: '#FFFFF',
      widget_title: '',
      widget_descciption: '',
      button_text: '',
      title_font_size: 'Medium',
      description_font_size: 'Medium',
      font_sizes: ['Extra Small', 'Small', 'Medium', 'Large', 'Extra Large']
    }
  }
  , methods: {
    updateWidgetTitle() {

    },
    updateWidgetDescription() {

    },
    updateButtonText() {

    }
  }
}
</script>

<style scoped>

#btn_cancel {
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

#btn_save {
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

#text_settings {
  padding-bottom: 30px;
}

#text_settings svg {
  width: 12px;
  height: 12px;
}

#text_settings p {
  width: 81px;
  height: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 22px;
  /* identical to box height, or 110% */
  color: #000000;
  align-content: center;

}

#text_general_configuration {
  display: flex;
  padding-bottom: 25px;
}

#text_general_configuration p {
  width: 506px;
  height: 28px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-size: 18px;
  line-height: 28px;
  display: flex;
  align-items: center;
  color: #202223;
  flex: none;
  order: 1;
  flex-grow: 1;

}

#text_general_configuration svg {
  width: 12px;
  height: 12px;
  padding-right: 5px;
}

#widget_title {
  padding-bottom: 18px;
}

#widget_title p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 10px;
}

#widget_title input {
  box-sizing: border-box;
  width: 421px;
  height: 40px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

#title_color_and_font-size {
  padding-bottom: 36px;
  display: flex;
  justify-content: space-between;
}

#title_color p {
  /* Title Color */
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  padding-bottom: 18px;
  color: #000000;
}

#title_color input[type="text"] {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#title_font_size p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  padding-bottom: 18px;
  color: #000000;
}

#title_font_size select {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#widget_description {
  padding-bottom: 18px;
}

#widget_description p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 10px;
}

#widget_description input {
  box-sizing: border-box;
  width: 421px;
  height: 40px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

#description_color_and_font-size {
  padding-bottom: 36px;
  display: flex;
  justify-content: space-between;
}

#description_color p {
  /* Title Color */
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  padding-bottom: 18px;
  color: #000000;
}


#description_color input[type="text"] {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#description_font_size p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  padding-bottom: 18px;
  color: #000000;
}

#description_font_size select {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#layout_style p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 24px;
}

#number_of_product p {
  width: 221px;
  height: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 17px;
}

#number_of_product input {
  /* Text holder */
  box-sizing: border-box;
  /* Auto layout */
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0px 0px 0px 12px;
  width: 134px;
  height: 36px;
  background: #FFFFFF;
  /* Grey 2 */
  border: 1px solid #C8C8C8;
  border-radius: 4px;
}

#layout_and_number {
  padding-bottom: 33px;
  justify-content: space-between;
}

#text_button_configuration {
  padding-bottom: 30px;
  display: flex;
}

#text_button_configuration p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-size: 18px;
  line-height: 28px;
  /* identical to box height, or 156% */
  display: flex;
  align-items: center;
  color: #202223;
}

#text_button_configuration svg {
  width: 12px;
  height: 12px;
  padding-right: 5px;
}

#button_text {
  padding-bottom: 30px;
}

#button_text p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 10px;
}

#button_text input {
  width: 423px;
  height: 40px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

#button_text_color {
  padding-bottom: 9px;
}

#button_text_color p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 30px;
}

#button_text_color input[type="text"] {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#button_bg_color p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 30px;
}

#button_bg_color input[type="text"] {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}


#button_border_color input[type="text"] {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 12px;
  gap: 10px;
  width: 190px;
  height: 36px;
  background: #FFFFFF;
  border: 1px solid #C9CCCF;
  border-radius: 4px;
}

#button_border_color p {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */
  color: #000000;
  padding-bottom: 30px;
}

.option_style {

  width: 74px;
  height: 22px;

  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 22px;
  /* identical to box height, or 157% */
  align-items: center;
  /* Character/Title .85 */

  color: rgba(0, 0, 0, 0.85);

  /* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;
}

.color_input {
  width: 30px;
  overflow: hidden;
  height: 30px;
  border-radius: 50%;
  margin-right: 20px;
}

.color_input input {
  width: 200%;
  height: 200%;
  cursor: pointer;
  margin-top: -15px;
  margin-left: -15px
}
#text_preview{
flex-direction: row;
align-items: center;
padding: 0px;
gap: 10px;
width: 501px;
height: 45px;


}
</style>