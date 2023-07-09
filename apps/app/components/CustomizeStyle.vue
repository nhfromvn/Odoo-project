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
            <img style="width: 100%;height: 100%" :src="style.example_image_url1"/>
          </div>
        </div>
        <div class="swatch_square">
          <div>
            <img style="width: 100%;height: 100%" :src="style.example_image_url2"/>
          </div>
        </div>
      </div>
      <div v-if="style.type=='Swatch in pill'" style="display: flex;gap: 15px;padding: 10px">
        <div :style="{borderColor:style.selected_button_border,
                                backgroundColor: style.selected_button_background_color
                                }" class="pill_selected">
          <div :style="{border:style.selected_button_swatch_border+' 1px solid',
                                borderRadius:'50%'}">
            <img :src="style.example_image_url1" class="image_round">
          </div>
          <div :style="{color:style.selected_button_text_color}">
            {{ style.example_text1 }}
          </div>
        </div>
        <div class="pill">
          <div>
            <img :src="style.example_image_url2" class="image_round">
          </div>
          <div>
            {{ style.example_text2 }}
          </div>
        </div>
      </div>
      <div v-if="style.type=='Button'" style="display: flex;gap: 15px">
        <div @mouseenter="style.hover=true" @mouseleave="style.hover=false"
             v-if="!style.hover||style.animation=='no effect'" :style="{color:style.selected_button_text_color,
                backgroundColor:style.selected_button_background_color,
                borderColor:style.selected_button_border}" class="button_square_selected">
          <div>{{ style.example_text1 }}</div>
        </div>
        <div @mouseenter="style.hover=true" @mouseleave="style.hover=false"
             v-if="style.hover&&style.animation=='Increase size'" :style="{color:style.selected_button_text_color,
                backgroundColor:style.selected_button_background_color,
                borderColor:style.selected_button_border,
                transform: 'scale(1.2)'}" class="button_square_selected">
          <div>{{ style.example_text1 }}</div>
        </div>
        <div class="button_square">
          <div> {{ style.example_text2 }}</div>
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
                  <option v-for="option in ['no effect','Increase size']" :value=option>
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
                    <img style="width: 100%;height: 100%" :src="selected_style.example_image_url1"/>
                  </div>
                </div>
                <div class="swatch_square">
                  <div>
                    <img style="width: 100%;height: 100%" :src="selected_style.example_image_url2"/>
                  </div>
                </div>
              </template>
              <template v-if="selected_style.type=='Swatch in pill'">
                <div :style="{borderColor:selected_style.selected_button_border,
                                backgroundColor: selected_style.selected_button_background_color
                                }" class="pill_selected">
                  <div :style="{border:selected_style.selected_button_swatch_border+' 1px solid',
                                borderRadius:'50%'}">
                    <img :src="selected_style.example_image_url1" class="image_round">
                  </div>
                  <div :style="{color:selected_style.selected_button_text_color}">
                    {{ selected_style.example_text1 }}
                  </div>
                </div>
                <div class="pill">
                  <div>
                    <img :src="selected_style.example_image_url2" class="image_round">
                  </div>
                  <div>
                    {{ selected_style.example_text2 }}
                  </div>
                </div>
              </template>
              <template v-if="selected_style.type=='Button'">
                <div @mouseenter="selected_style.hover=true" @mouseleave="selected_style.hover=false"
                     v-if="!selected_style.hover||selected_style.animation=='no effect'" :style="{color:selected_style.selected_button_text_color,
                backgroundColor:selected_style.selected_button_background_color,
                borderColor:selected_style.selected_button_border}" class="button_square_selected">
                  <div>{{ selected_style.example_text1 }}</div>
                </div>
                <div @mouseenter="selected_style.hover=true" @mouseleave="selected_style.hover=false"
                     v-if="selected_style.hover&&selected_style.animation=='Increase size'" :style="{color:selected_style.selected_button_text_color,
                backgroundColor:selected_style.selected_button_background_color,
                borderColor:selected_style.selected_button_border,
                transform: 'scale(1.2)'}" class="button_square_selected">
                  <div>{{ selected_style.example_text1 }}</div>
                </div>
                <div class="button_square">
                  <div>{{ selected_style.example_text2 }}</div>
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
.Polaris-Card {
  box-shadow: var(--p-card-shadow, 0 0 0 1px rgba(63, 63, 68, 0.05), 0 1px 3px 0 rgba(63, 63, 68, 0.15));
  outline: 0.1rem solid transparent;
  background: #ffffff;
  padding: 20px;
  margin: 20px;
}

.swatch_square {
  padding: 5px;
  border: 1px #a3a3a3 solid;
  width: 80px;
  height: 80px;
}

.swatch_square_selected {
  padding: 5px;
  border: 2px #000000 solid;
  width: 80px;
  height: 80px;
}

.image_round {
  border-radius: 50%;
  width: 50px;
  height: 50px;
  overflow: hidden
}

.pill_selected {
  border-radius: 30px;
  display: flex;
  gap: 15px;
  border: 2px #000000 solid;
  padding: 10px;
  width: 150px;
  height: 60px;
  align-items: center;
}

.button_square_selected {
  padding: 5px;
  width: 50px;
  height: 50px;
  align-items: center;
  display: flex;
  border: #b2b2b2 2px solid;
  justify-content: center;
  background: black;
  color: #FFFFFF;
}

.pill {
  border-radius: 30px;
  display: flex;
  gap: 15px;
  border: 1px #a3a3a3 solid;
  padding: 10px;
  width: 150px;
  height: 60px;
  align-items: center;
}

.button_square {
  padding: 5px;
  width: 50px;
  height: 50px;
  align-items: center;
  display: flex;
  border: #a3a3a3 1px solid;
  justify-content: center;
}

.customize_line {
  display: flex;
  gap: 10px;
}

#preview_container {
  width: 100%;
}

#preview {
  box-shadow: var(--p-card-shadow, 0 0 0 1px rgba(63, 63, 68, 0.05), 0 1px 3px 0 rgba(63, 63, 68, 0.15));
  outline: 0.1rem solid transparent;
  background: #ffffff;
  padding: 20px;
  width: 100%;
  height: 500px;
}

#image_wrapper {
  display: flex;
  gap: 10px;
  justify-content: start;
  width: 100%;
}

.color_wrapper {
  height: 40px;
  width: 40px;
  border-radius: 25%;
  overflow: hidden;
  border: 1px solid black;
}

.color_wrapper input {

  border-radius: 0 !important;
  overflow: hidden;
  transform: translate(-25%, -25%)
}

#side_modal {
  box-shadow: var(--p-card-shadow, 0 0 0 1px rgba(63, 63, 68, 0.05), 0 1px 3px 0 rgba(63, 63, 68, 0.15));
  outline: 0.1rem solid transparent;
  background: #ffffff;
  padding: 20px;
  height: 500px;

}

#side_content {
  padding-left: 15px;
}

select {
  padding: 10px;

  box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgba(22, 29, 37, .05);
  text-size-adjust: 100%;
  fill: currentColor;
  -webkit-font-smoothing: antialiased;
  -webkit-box-direction: normal;
  font: inherit;
  text-transform: none;
  position: relative;
  background-color: #fff;
  border: .1rem solid #c4cdd5;
  border-radius: .3rem;
  color: #31373d;
  display: block;
  width: 100%;
  font-size: 15px;
  vertical-align: baseline;
  height: auto;
  margin: 0;
  max-width: 100%;
  font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
  box-sizing: border-box;
  transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
  appearance: none;
  padding-right: 3.2rem;
  background-image: url(data:image/svg+xml;charset=utf8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyMCAyMCc+PHBhdGggZmlsbD0ncmdiKDk5LDExNSwxMjkpJyBkPSdNMTMgOGwtMy0zLTMgM2g2em0tLjEgNEwxMCAxNC45IDcuMSAxMmg1Ljh6JyBmaWxsLXJ1bGU9J2V2ZW5vZGQnPjwvcGF0aD48L3N2Zz4=);
  background-position: right .7rem top .7rem;
  background-size: 21px 21px;
  background-repeat: no-repeat;
}

.ant-modal-close-icon svg {
  margin: 20px !important;;
}
</style>