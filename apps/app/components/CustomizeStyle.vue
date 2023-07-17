<script>
import {defineComponent} from 'vue'
import {Modal} from "ant-design-vue";

export default defineComponent({
  name: "CustomizeStyle",
  components: {Modal},
  props: {
    proptemp: Object
  },
  data() {
    return {
      show_modal: false,
      selected_style: null,
    }
  }, methods: {
    save(style) {
      this.$emit('saveStyle', style)
    },
    showModal(style) {
      this.show_modal = true
      this.selected_style = style
    }
  }, mounted() {
    for (let style of this.proptemp) {
      if (style.type == 'Button') {
        style.hover = false
      }
    }
  }
})
</script>

<template>
  <h2>Customize style for variant option</h2>
  <div v-for="style in proptemp" class="Polaris-Card">
    <div style="display: flex; justify-content: space-between">
      <div> {{ style.type }}</div>
      <div style="display: flex;">
        <a @click="showModal(style)">Customize</a>

        <p v-if="style.in_use">(In use)</p>
      </div>
    </div>
    <div style="display: flex; margin:10px">
      <div v-if="style.type=='Square swatch'" style="display: flex;gap: 15px;padding: 10px">
        <div class="swatch_square_selected" :style="{borderColor:style.selected_swatch_outer_border}">
          <div style="border: 2px solid" :style="{borderColor:style.selected_swatch_inner_border}">
            <img style="width: 100%;height: 100%" :src="style.example_image_url_selected"/>
          </div>
        </div>
        <div class="swatch_square">
          <div>
            <img style="width: 100%;height: 100%" :src="style.example_image_url_unselected"/>
          </div>
        </div>
      </div>
      <div v-if="style.type=='Swatch in pill'" style="display: flex;gap: 15px;padding: 10px">
        <div :style="{borderColor:style.selected_button_border,
                                backgroundColor: style.selected_button_background_color
                                }" class="pill_selected">
          <div :style="{border:style.selected_button_swatch_border+' 1px solid',
                                borderRadius:'50%'}">
            <img :src="style.example_image_url_selected" class="image_round">
          </div>
          <div :style="{color:style.selected_button_text_color}">
            {{ style.example_text_selected }}
          </div>
        </div>
        <div class="pill">
          <div>
            <img :src="style.example_image_url_unselected" class="image_round">
          </div>
          <div>
            {{ style.example_text_unselected }}
          </div>
        </div>
      </div>
      <div v-if="style.type=='Button'" style="display: flex;gap: 15px">
        <div @mouseenter="style.hover=true" @mouseleave="style.hover=false"
             v-if="!style.hover||style.animation=='no effect'" :style="{color:style.selected_button_text_color,
                backgroundColor:style.selected_button_background_color,
                borderColor:style.selected_button_border}" class="button_square_selected">
          <div>{{ style.example_text_selected }}</div>
        </div>
        <div @mouseenter="style.hover=true" @mouseleave="style.hover=false"
             v-if="style.hover&&style.animation=='Increase size'" :style="{color:style.selected_button_text_color,
                backgroundColor:style.selected_button_background_color,
                borderColor:style.selected_button_border,
                transform: 'scale(1.2)'}" class="button_square_selected">
          <div>{{ style.example_text_selected }}</div>
        </div>
        <div @mouseenter="style.hover=true" @mouseleave="style.hover=false"
             v-if="style.hover&&style.animation=='Shadow'" :style="{color:style.selected_button_text_color,
                backgroundColor:style.selected_button_background_color,
                borderColor:style.selected_button_border,
                boxShadow: '0 10px 4px rgba(0, 0, 0, 0.1)',}" class="button_square_selected">
          <div>{{ style.example_text_selected }}</div>
        </div>
        <div class="button_square">
          <div> {{ style.example_text_unselected }}</div>
        </div>
      </div>
    </div>
    <Modal id="post_modal_wrapper"
           style="width: 70%;height: 100%"
           :footer="null"
           v-model:visible="show_modal"
           :maskClosable="false"
           @cancel="show_modal=false;">
      <div style="display: flex; gap:30px">
        <div>
          <div>
            {{ selected_style.type }}
          </div>
          <div id="side_modal">
            <div>Selected {{ selected_style.type }}</div>
            <div id="side_content">
              <template v-if="selected_style.type=='Square swatch'">
                <label>Outer border</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input
                        v-model="selected_style.selected_swatch_outer_border" type="color"/></div>

                  <input type="text" class="input_setting"
                         v-model="selected_style.selected_swatch_outer_border"/>
                </div>
                <label>Inner border</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_swatch_inner_border"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_swatch_inner_border"/>
                </div>
              </template>
              <template v-if="selected_style.type=='Swatch in pill'">
                <label>Text color</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_text_color"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_text_color"/>
                </div>
                <label>Button border</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_border"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_border"/>
                </div>
                <label>Swatch border</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_swatch_border"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_swatch_border"/>
                </div>
                <label>Background color</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_background_color"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_background_color"/>
                </div>
              </template>
              <template v-if="selected_style.type=='Button'">
                <label>Button border</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_border"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_border"/>
                </div>
                <label>Text color</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_text_color"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_text_color"/>
                </div>
                <label>Background color</label>
                <div class="customize_line">
                  <div class="color_wrapper">
                    <input type="color"
                           v-model="selected_style.selected_button_background_color"/>
                  </div>
                  <input class="input_setting" type="text" v-model="selected_style.selected_button_background_color"/>
                </div>
                <label>Animation</label>
                <br>
                <select v-model="selected_style.animation">
                  <option v-for="option in ['no effect','Increase size','Shadow']" :value=option>
                    {{ option }}
                  </option>
                </select>
              </template>
            </div>
          </div>
        </div>
        <div id="preview_container">
          <div>Preview</div>
          <div id="preview">
            <h3 style="margin: 0px 0px 20px 0px">{{ selected_style.example_option }}:</h3>
            <div id="image_wrapper">
              <template v-if="selected_style.type=='Square swatch'">
                <div class="swatch_square_selected" :style="{borderColor:selected_style.selected_swatch_outer_border}">
                  <div style="border: 2px solid" :style="{borderColor:selected_style.selected_swatch_inner_border}">
                    <img style="width: 100%;height: 100%" :src="selected_style.example_image_url_selected"/>
                  </div>
                </div>
                <div class="swatch_square">
                  <div>
                    <img style="width: 100%;height: 100%" :src="selected_style.example_image_url_unselected"/>
                  </div>
                </div>
              </template>
              <template v-if="selected_style.type=='Swatch in pill'">
                <div :style="{borderColor:selected_style.selected_button_border,
                                backgroundColor: selected_style.selected_button_background_color
                                }" class="pill_selected">
                  <div :style="{border:selected_style.selected_button_swatch_border+' 1px solid',
                                borderRadius:'50%'}">
                    <img :src="selected_style.example_image_url_selected" class="image_round">
                  </div>
                  <div :style="{color:selected_style.selected_button_text_color}">
                    {{ selected_style.example_text_selected }}
                  </div>
                </div>
                <div class="pill">
                  <div>
                    <img :src="selected_style.example_image_url_unselected" class="image_round">
                  </div>
                  <div>
                    {{ selected_style.example_text_unselected }}
                  </div>
                </div>
              </template>
              <template v-if="selected_style.type=='Button'">
                <div @mouseenter="selected_style.hover=true" @mouseleave="selected_style.hover=false"
                     v-if="!selected_style.hover||selected_style.animation=='no effect'" :style="{color:selected_style.selected_button_text_color,
                backgroundColor:selected_style.selected_button_background_color,
                borderColor:selected_style.selected_button_border,
                   }" class="button_square_selected">
                  <div>{{ selected_style.example_text_selected }}</div>
                </div>
                <div @mouseenter="selected_style.hover=true" @mouseleave="selected_style.hover=false"
                     v-if="selected_style.hover&&selected_style.animation=='Increase size'" :style="{color:selected_style.selected_button_text_color,
                backgroundColor:selected_style.selected_button_background_color,
                borderColor:selected_style.selected_button_border,

                transform: 'scale(1.2)'
                     }" class="button_square_selected">
                  <div>{{ selected_style.example_text_selected }}</div>
                </div>
                 <div @mouseenter="selected_style.hover=true" @mouseleave="selected_style.hover=false"
                     v-if="selected_style.hover&&selected_style.animation=='Shadow'" :style="{color:selected_style.selected_button_text_color,
                backgroundColor:selected_style.selected_button_background_color,
                borderColor:selected_style.selected_button_border,
               boxShadow: '0 10px 4px rgba(0, 0, 0, 0.1)'
                     }" class="button_square_selected">
                  <div>{{ selected_style.example_text_selected }}</div>
                </div>
                <div class="button_square">
                  <div>{{ selected_style.example_text_unselected }}</div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
      <div style="width: 100%;display: flex;justify-content: end;gap:20px;margin-top: 20px">
        <button @click="show_modal=false">Cancel</button>
        <button @click="save(selected_style)">Save</button>
      </div>
    </Modal>
  </div>
</template>

<style scoped>

</style>