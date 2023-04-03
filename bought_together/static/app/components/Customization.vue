<template>
  <div class="container" id="container">
    <div class="d-flex justify-content-center">
      <div id="frame_427319039">
        <button class="head_btn" id="add_product" @click="goTo('add_product')">Add Product</button>
        <button class="head_btn is_select" id="customization">Customization</button>
        <button class="head_btn" id="installation" @click="goTo('installation')">Installation</button>
      </div>
    </div>
    <div class="d-flex justify-content-end">
      <div class="right_top_btns" style="display: flex; gap: 19px">
        <button id="btn_cancel" @click="cancel()">
          Cancel
        </button>
        <button id="btn_save" @click="save()">
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
          <input type="text" v-model="widget_title">
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
              <option class="option_style" v-for="option in font_sizes" :value="option">{{ option.name }}</option>
            </select></div>
        </div>
        <div id="widget_description">
          <p>Widget Description</p>
          <input type="text" v-model="widget_description">
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
              <option class="option_style" v-for="option in font_sizes" :value="option">{{ option.name }}</option>
            </select></div>
        </div>
        <div id="layout_and_number" style="display: flex">
          <div id="layout_style">
            <p>Layout Style</p>
            <li>List</li>
          </div>
          <div id="number_of_product">
            <p>Number of products to show</p>
            <input v-model="numbers_product" type="number" min="1" max="5">
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
          <input type="text" v-model="button_text">
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
      </div>
      <div id="content_right">
        <div id="text_preview" class="d-flex align-items-center">
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>Preview</p>
        </div>
        <div id="rectangle_preview" style="justify-content: center">
          <div id="show_widget_title" :style="{
            color: title_color,
            fontSize: title_font_size.value}">{{ widget_title }}
          </div>
          <div id="show_widget_description" :style="{
            color: description_color,
            fontSize: description_font_size.value}">{{ widget_description }}
          </div>
          <div style="display: flex;
                      justify-content: space-around">
            <div id="images">
              <div v-for="product in list_recommend_product">
                <div style="display: flex" v-if="list_recommend_product.indexOf(product)<numbers_product">
                <img style="width: 65px;
                        height: 61px;" :src="product.image_url"/>
                <div style="padding: 9px"
                     v-if="list_recommend_product.indexOf(product)!=numbers_product-1"
                     class="d-flex align-items-center">
                  <font-awesome-icon :icon="['fas', 'plus']"/>
                </div>
                </div>
              </div>
            </div>
            <div>
              <div id="total_price">
                <p>Total: </p>
                <p id="show_total_price">${{ total_price }}</p>
              </div>
              <button id="show_button" :style=" {color: btn_text_color,
                                                 backgroundColor: btn_bg_color,
                                                 borderColor:btn_border_color}">
                {{ button_text }}
              </button>
            </div>
          </div>

          <div v-for="product in list_recommend_product" >
            <div class="products"  v-if="list_recommend_product.indexOf(product)<numbers_product">
            <div  style="display: flex;
                        gap:14px">
              <input type="checkbox">
              <p>{{ product.name }}</p>
            </div>
            <div class="product_price">
              <div style="display: flex
                     ;gap: 18px">
                <div v-if="product.compare_at_price">${{ product.compare_at_price }}</div>
                <div v-else>${{ product.price }}</div>
              </div>
            </div>
            </div>
          </div>
          <div>
          </div>
          <p style="font-family: 'Inter';
                  font-style: normal;
                  font-weight: 600;
                  font-size: 12px;
                  line-height: 22px;
                  text-decoration-line: line-through;
                  display: flex;
                  justify-content: right">
            ${{ sub_total_price }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Customization",
  props: {
    list_recommend_product: Array,
    list_exclude_product: Array
  },
  data() {
    return {
      btn_text_color: '#FFFFFF',
      btn_bg_color: '#0000FF',
      btn_border_color: '#b0a161',
      description_color: '#000000',
      title_color: '#000000',
      widget_title: 'YOU MAY ALSO LIKE...',
      widget_description: 'Good deals only for you!',
      button_text: 'Add to cart',
      numbers_product: 3,
      title_font_size: {
        name: 'Medium', value: 18
      },
      description_font_size: {
        name: 'Small', value: 16
      },
      font_sizes: [{
        name: 'Extra Small', value: 12
      }, {
        name: 'Small', value: 16
      }, {
        name: 'Medium', value: 18
      }, {
        name: 'Large', value: 20
      }, {
        name: 'Extra Large', value: 25
      }],
    }
  },
  methods: {
    goTo(id){
      this.$emit("goTo",id)
    },
    save() {
      let params = {
        widget_title: this.widget_title,
        widget_description: this.widget_description,
        product_included:  this.numbers_product,
        total_price:this.total_price
      }
      this.$emit('saveCustomization',params)
      console.log(params)
    },
    cancel() {

    }
  },
  computed: {
    total_price: function () {
      let price = 0
      for (let product of this.list_recommend_product) {
        price += Number(product.price)
      }
      return price
    },
    sub_total_price: function () {
      let price = 0
      for (let product of this.list_recommend_product) {
        if (product.compare_at_price) {
          price += Number(product.compare_at_price)
        } else {
          price += Number(product.price)
        }
      }
      return price
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
  border: 2px solid;
}

.color_input input {
  width: 200%;
  height: 200%;
  cursor: pointer;
  margin-top: -15px;
  margin-left: -15px
}

#text_preview {
  flex-direction: row;
  align-items: center;
  padding: 0px;
  gap: 10px;
  width: 501px;
  height: 45px;
}

#show_widget_title {
  height: 24px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  line-height: 22px;
  /* or 110% */
  text-align: center;
  color: #000000;
  margin-bottom: 26px;
}

#show_widget_description {
  height: 25px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 22px;
  /* or 157% */
  text-align: center;
  color: #000000;
  margin-bottom: 26px;
}

#images {
  display: flex;
  margin-bottom: 30px;
}

#rectangle_preview {
  box-sizing: border-box;
  width: 533px;
  background: #FFFFFF;
  border: 1px solid #BFBFBF;
  border-radius: 5px;
  padding: 9px;
}

#total_price {
  height: 18px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 22px;
  /* or 138% */
  text-align: center;
  color: #000000;
  display: flex;
  justify-content: center;
  gap: 5px;
  margin: 10px;
}

#total_price #show_total_price {
  color: #FF0000;
}

#show_button {
  width: 183px;
  height: 24px;
  border-radius: 3px;
  font-family: 'Inter';
  font-style: normal;
  font-size: 16px;
  line-height: 22px;
  margin-bottom: 20px;
}

.product_price {
  text-align: center;
  color: #ff0000;
  padding: 12px;
}

.products {
  display: flex;
  justify-content: space-around;
  gap: 14px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 17px;
  padding: 10px;
  margin-right: 30px;
}

.products p {
  flex-wrap: wrap;
  align-content: center;
}
</style>