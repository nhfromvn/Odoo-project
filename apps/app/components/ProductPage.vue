<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "ProductPage",
  data() {
    return {
      product: null,
      option: null,
      value: null
    }
  },
  props: {
    att_product_page: Object,
    temp: Object,
    product_id: String,
  }, mounted() {
    let self = this
    this.product = this.temp.products.find(product => product.product_id == this.product_id)
    this.product.options.forEach(function (option) {
      option.setting = self.temp.options.find(e => e.name == option.name)
      console.log(self.product)
    })
    console.log(this.product_id)
    for (let option of this.product.options) {
      option.selected = option.values[0]
      option.values.forEach(function (e) {
        e.hover = false
      })
      console.log(option.setting.product_style)
    }
    this.option = this.product.options.find(e => e.name == this.att_product_page.option_name)
    this.value = this.option.values.find(e => e.name == this.att_product_page.value)
    console.log(this)
  }
})
</script>
<template>
  <label :for="att_product_page.att_for">
      <template v-if="option">
        <template v-if="option.setting.product_style=='Square swatch'">
          <label  v-if="option.selected==value"
                 class="swatch_square_selected"
                 :style="{borderColor:temp.styles.swatch.selected_swatch_outer_border}">
            <div style="border: 2px solid;width: 100%;height: 100%"
                 :style="{borderColor:temp.styles.swatch.selected_swatch_inner_border}">
              <img style="width: 100%;height: 100%" :src="value.image_url"/>
            </div>
          </label>
          <label  v-else
                 @click="option.selected=value" class="swatch_square">
            <div style="width: 100%;height: 100%">
              <img style="width: 100%;height: 100%" :src="value.image_url"/>
            </div>
          </label>
        </template>
        <template v-if="option.setting.product_style=='Swatch in pill'">
          <label v-if="option.selected==value" :style="{borderColor:temp.styles.swatch_in_pill.selected_button_border,
                                                backgroundColor: temp.styles.swatch_in_pill.selected_button_background_color
                                                }" class="pill_selected">
            <div :style="{border:temp.styles.swatch_in_pill.selected_button_swatch_border+' 1px solid',
                                                borderRadius:'50%'}">
              <img :src="value.image_url" class="image_round">
            </div>
            <div :style="{color:temp.styles.swatch_in_pill.selected_button_text_color}">
              {{ value.name }}
            </div>
          </label>
          <label v-else
                 @click="option.selected=value" class="pill">
            <div>
              <img :src="value.image_url" class="image_round">
            </div>
            <div>
              {{ value.name }}
            </div>
          </label>
        </template>
        <template v-if="option.setting.product_style=='Button'">
          <template v-if="temp.styles.button.animation">
            <label  v-if="option.selected==value&&!value.hover"
                   @mouseenter="value.hover=true;"

                   :style="{color:temp.styles.button.selected_button_text_color,
                                backgroundColor:temp.styles.button.selected_button_background_color,
                                borderColor:temp.styles.button.selected_button_border}" class="button_square_selected">
              <div>{{ value.name }}</div>
            </label>
            <label v-if="option.selected==value&&value.hover"

                   @mouseleave="value.hover=false"
                   :style="{color:temp.styles.button.selected_button_text_color,
                                backgroundColor:temp.styles.button.selected_button_background_color,
                                borderColor:temp.styles.button.selected_button_border,
                                transform: 'scale(1.2)'}"
                   class="button_square_selected">
              <div>{{ value.name }}</div>
            </label>
            <label v-if="option.selected!=value"
                   @click="option.selected=value" class="button_square">
              <div> {{ value.name }}</div>
            </label>
          </template>
          <template v-else>
            <label v-if="option.selected==value"
                   :style="{color:temp.styles.button.selected_button_text_color,
                                backgroundColor:temp.styles.button.selected_button_background_color,
                                borderColor:temp.styles.button.selected_button_border}" class="button_square_selected">
              <div>{{ value.name }}</div>
            </label>
            <label v-else
                   @click="option.selected=value" class="button_square">
              <div> {{ value.name }}</div>
            </label>
          </template>
        </template>
      </template>
  </label>
</template>

<style scoped>

</style>