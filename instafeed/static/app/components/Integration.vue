<template>
  <div id="navBar">
    <div>
      <button id="btn_connect" style="display: flex; gap:5px" @click="connect_instagram">
        <font-awesome-icon :icon="['fab', 'instagram']"/>
        <p>Add Instagram Account</p>
      </button>
      <div>
        {{ proptemp.instagram_count }} connected
      </div>
      <div v-if="username" style="display: flex"><p>Connected to {{ username }} with instagram</p>
        <p style="margin: 0px 5px">|</p>
        <a @click="changeAccount()">Change account</a></div>
    </div>
    <div>
      <button id="btn_connect_fb" style="display: flex; gap:5px" @click="connect_facebook">
        <font-awesome-icon icon="fa-brands fa-facebook-f"
                           style="color: white"/>
        <p>Add Facebook Account</p>
      </button>
      <div style="    padding-top: 0.75em;
                      padding-bottom: 0.3em;
                      color: rgba(0, 0, 0, 0.45);
                      text-align: left;
                      caption-side: bottom;
                      font-size: 10px;">
        Add Facebook Account to explore advance feature
      </div>
      <div>
        {{ proptemp.facebook_count }} connected
      </div>
      <div v-if="fb_username" style="display: flex"><p>Connected to {{ fb_username }} with facebook</p>
        <p style="margin: 0px 5px">|</p>
      </div>
    </div>
  </div>
</template>
<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Integration",
  props: {
    proptemp: Object
  },
  methods: {
    connect_facebook() {
      let self = this
      window.location.href = '/instafeed/facebook/connect'
    },
    connect_instagram() {
      window.location.href = '/instafeed/connect'
    },
  }
})
</script>


<style scoped>

#navBar {
  display: flex;
  box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
  margin-bottom: 2rem;
  background-color: #ffffff;
  padding: 20px;
  gap: 30px;
  position: relative;
  height: auto;
}

#btn_connect {
  color: #ffffff;
  align-items: center;
  flex-wrap: wrap !important;
  border-radius: 4px;
  background: rgb(0 128 96);
  border: 0.1rem solid transparent;
  box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
  font-weight: 400;
  margin: 3px;
  display: inline-block;
  justify-content: center;
  padding: 7px 16px;
  cursor: pointer;
  white-space: nowrap;
  text-transform: none;
  font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
}

#btn_connect_fb {
  color: #ffffff;
  align-items: center;
  flex-wrap: wrap !important;
  border-radius: 4px;
  background: rgb(0, 30, 128);
  border: 0.1rem solid transparent;
  box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
  font-weight: 400;
  margin: 3px;
  display: inline-block;
  justify-content: center;
  padding: 7px 16px;
  cursor: pointer;
  white-space: nowrap;
  text-transform: none;
  font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
}
</style>