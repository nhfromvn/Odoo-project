<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "ConfigVariantOption",
  props: {
    proptemp: Object
  },
  data() {
    return {
      search_recommendation: '',
    }
  },
  methods: {
    saveData() {
      this.$emit('saveData', this.proptemp)
    }
  },
  computed: {
    filteredRows: function () {
      let self = this
      return self.proptemp.options.filter(function (option) {
        return String(option.name).toLowerCase().indexOf(self.search_recommendation.toLowerCase()) > -1
      })
    }
  }
})
</script>

<template>
  <div>
    <div style="display:flex;justify-content: space-between">
      <h2>
        Config Variant Option Style
      </h2>
      <button @click="saveData">
        Save
      </button>
    </div>

    <div>Control how you want to show each product option in product and collection pages</div>
    <div style="border: solid #000000 1px; padding: 20px 20px 0px 20px;margin: 0px 0px 20px 0px">
      <input id="search_bar" v-model="search_recommendation"
             placeholder="Search option by name"
      />
      <hr>
      <div v-for="option in filteredRows" style="margin-bottom: 20px">
        <div><b>{{ option.name }} </b>(affects {{ option.product_affect }} product)
        </div>
        <div style="margin-left: 30px" class="">
          <div>Display style on products:</div>
          <div class="option_line">
            <select class="variant_style_select" v-model="option.product_style">
              <option class="variant_style_option" v-for="style in proptemp.styles" :value="style.type">
                {{ style.type }}
              </option>
            </select>
            <select v-model="option.product_page_swatch_image"
                    v-if="option.product_style.toLowerCase().includes('swatch')">
              <option v-for="val in ['Use 1st image of variant','Use 2st image of variant','Use last image of variant']"
                      :value="val">
                {{ val }}
              </option>
            </select>
          </div>
          <div>Display style on collections:</div>
          <div class="option_line">
            <select class="variant_style_select" v-model="option.collection_style">
              <option class="variant_style_option" v-for="style in proptemp.styles" :value="style.type">
                {{ style.type }}
              </option>
            </select>
            <select v-model="option.collection_page_swatch_image"
                    v-if="option.collection_style.toString().includes('swatch')">
              <option v-for="val in ['Use 1st image of variant','Use 2st image of variant','Use last image of variant']"
                      :value="val">
                {{ val }}
              </option>
            </select>
          </div>
<!--          <div>Prevent default selection</div>-->
<!--          <div style="display: flex; gap: 10px"><input type="checkbox" v-model="option.prevent_default">Make your-->
<!--            customer choose this option manually,-->
<!--            before adding item to the cart-->
<!--          </div>-->
        </div>
      </div>

    </div>
    <div style="border: solid #000000 1px; padding: 20px 20px 20px 20px">
      <h2>Low stock alert</h2>
      <div>Add an alert to the product page if the inventory of a variant falls below threshold level. This creates an
        urgency and helps to sell products faster. You can add this alert using the "Low Stock Alert" app block.
      </div>
      <div class="general_line">
        <label>Inventory threshold</label>
        <input type="number" v-model="proptemp.general.inventory_threshold"/>
      </div>
      <div class="general_line">
        <label>Notification message</label>
        <input type="text" v-model="proptemp.general.notification_message"/>
      </div>
      <h2>Text settings for manually selected options</h2>
      <div class="general_line">
        <label>Option label text when a value is not selected</label>
        <input type="text" v-model="proptemp.general.option_label"/>
      </div>
      <div class="general_line">
        <label>"Add to cart" button text when an option is not selected</label>
        <input type="text" v-model="proptemp.general.add_to_cart_label"/>
      </div>
    </div>
  </div>

</template>

<style scoped>
#search_bar {
  display: block;
  margin-bottom: 0px !important;
  box-sizing: border-box;
  width: 100%;
  height: 30px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

.variant_style_select {

  height: 100%;
}

.variant_style_option {
  height: 100%;
}

.general_line {
  display: flex;
  gap: 20px;
  align-items: center;
  margin: 10px;
}

.general_line input {
  text-size-adjust: 100%;
  fill: currentColor;
  -webkit-font-smoothing: antialiased;
  -webkit-box-direction: normal;
  padding: .5rem 1rem;
  background-color: #fff;
  border: .1rem solid #c4cdd5;
  border-radius: .3rem;
  color: #31373d;
  display: block;
  font-size: 15px;
  width: 100%;
  vertical-align: baseline;
  height: auto;
  margin: 0;
  max-width: 40%;
  font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
  box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgba(22, 29, 37, .05);
  box-sizing: border-box;
  transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
  appearance: none;
}

.option_line {
  display: flex;
  gap: 20px
}

.option_line select {
  padding: 10px;
  background-size: 21px 21px;
  background-repeat: no-repeat;
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
  margin: 10px 0px;
  max-width: 40%;
  font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
  box-sizing: border-box;
  transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
  appearance: none;
  padding-right: 3.2rem;
  background-image: url(data:image/svg+xml;charset=utf8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyMCAyMCc+PHBhdGggZmlsbD0ncmdiKDk5LDExNSwxMjkpJyBkPSdNMTMgOGwtMy0zLTMgM2g2em0tLjEgNEwxMCAxNC45IDcuMSAxMmg1Ljh6JyBmaWxsLXJ1bGU9J2V2ZW5vZGQnPjwvcGF0aD48L3N2Zz4=);
  background-position: right .7rem top .7rem;
}
</style>