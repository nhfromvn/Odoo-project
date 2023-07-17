<script>
import {defineComponent} from 'vue'
export default defineComponent({
  name: "CollectionPage",
  props: {
    product_id: String,
    temp: Object
  },

  data() {
    return {
      product: {},
    }
  },
  mounted() {
    let self = this
    this.product = this.temp.products.find(product => product.product_id == this.product_id)
    console.log(this.product)
    this.product.options.forEach(function (option) {
      option.setting = self.temp.options.find(e => e.name == option.name)
      console.log(self.product)
    })
    for (let option of this.product.options) {
      option.selected = option.values[0]
      option.values.forEach(function (e) {
        e.hover = false
      })

    }
  }
})
</script>

<template>
  <div style="z-index: 2;position: relative">
    <template v-for="option in product.options">
      <div style="display: flex; margin:10px">
        <div v-if="option.setting.collection_style=='Square swatch'" style="display: flex;gap: 15px;padding: 10px">
          <template v-for="option_value in option.values">
            <div v-if="option.selected==option_value"
                 style="z-index: 5;position: relative"
                 class="swatch_square_selected"
                 :style="{borderColor:temp.styles.swatch.selected_swatch_outer_border}">
              <div style="border: 2px solid;width: 100%;height: 100%"
                   :style="{borderColor:temp.styles.swatch.selected_swatch_inner_border}">
                <img style="width: 100%;height: 100%" :src="option_value.image_url"/>
              </div>
            </div>
            <div v-else
                 @click="option.selected=option_value" class="swatch_square">
              <div style="width: 100%;height: 100%">
                <img style="width: 100%;height: 100%" :src="option_value.image_url"/>
              </div>
            </div>
          </template>
        </div>
        <div v-if="option.setting.collection_style=='Swatch in pill'" style="display: flex;gap: 15px;padding: 10px">
          <template v-for="option_value in option.values">
            <div v-if="option.selected==option_value" :style="{borderColor:temp.styles.swatch_in_pill.selected_button_border,
                                  backgroundColor: temp.styles.swatch_in_pill.selected_button_background_color
                                  }" class="pill_selected">
              <div :style="{border:temp.styles.swatch_in_pill.selected_button_swatch_border+' 1px solid',
                                  borderRadius:'50%'}">
                <img :src="option_value.image_url" class="image_round">
              </div>
              <div :style="{color:temp.styles.swatch_in_pill.selected_button_text_color}">
                {{ option_value.name }}
              </div>
            </div>
            <div v-else
                 @click="option.selected=option_value" class="pill">
              <div>
                <img :src="option_value.image_url" class="image_round">
              </div>
              <div>
                {{ option_value.name }}
              </div>
            </div>
          </template>
        </div>
        <div v-if="option.setting.collection_style=='Button'" style="display: flex;gap: 15px;padding: 10px;">
          <template v-for="option_value in option.values">
            <template v-if="temp.styles.button.animation">
              <div v-if="option.selected==option_value&&!option_value.hover"
                   @mouseenter="option_value.hover=true;"

                   :style="{color:temp.styles.button.selected_button_text_color,
                  backgroundColor:temp.styles.button.selected_button_background_color,
                  borderColor:temp.styles.button.selected_button_border}" class="button_square_selected">
                <div>{{ option_value.name }}</div>
              </div>
              <div v-if="option.selected==option_value&&option_value.hover"
                   @mouseleave="option_value.hover=false"
                   :style="{color:temp.styles.button.selected_button_text_color,
                  backgroundColor:temp.styles.button.selected_button_background_color,
                  borderColor:temp.styles.button.selected_button_border,
                  transform: 'scale(1.2)',
                   boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'}"
                   class="button_square_selected">
                <div>{{ option_value.name }}</div>
              </div>
              <div v-if="option.selected!=option_value"
                   @click="option.selected=option_value" class="button_square">
                <div> {{ option_value.name }}</div>
              </div>
            </template>
            <template v-else>
              <div v-if="option.selected==option_value"
                   :style="{color:temp.styles.button.selected_button_text_color,
                  backgroundColor:temp.styles.button.selected_button_background_color,
                  borderColor:temp.styles.button.selected_button_border}" class="button_square_selected">
                <div>{{ option_value.name }}</div>
              </div>
              <div v-else
                   @click="option.selected=option_value" class="button_square">
                <div> {{ option_value.name }}</div>
              </div>
            </template>
          </template>
        </div>
      </div>
    </template>
  </div>
</template>
<!--todo-->
<!--tach css ra file rieng, dung thu vien antd de chia layout-->
<style scoped>

</style>