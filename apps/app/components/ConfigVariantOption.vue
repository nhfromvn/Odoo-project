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
<!--    <div style="border: solid #000000 1px; padding: 20px 20px 20px 20px">-->
<!--      <h2>Low stock alert</h2>-->
<!--      <div>Add an alert to the product page if the inventory of a variant falls below threshold level. This creates an-->
<!--        urgency and helps to sell products faster. You can add this alert using the "Low Stock Alert" app block.-->
<!--      </div>-->
<!--      <div class="general_line">-->
<!--        <label>Inventory threshold</label>-->
<!--        <input type="number" v-model="proptemp.general.inventory_threshold"/>-->
<!--      </div>-->
<!--      <div class="general_line">-->
<!--        <label>Notification message</label>-->
<!--        <input type="text" v-model="proptemp.general.notification_message"/>-->
<!--      </div>-->
<!--      <h2>Text settings for manually selected options</h2>-->
<!--      <div class="general_line">-->
<!--        <label>Option label text when a value is not selected</label>-->
<!--        <input type="text" v-model="proptemp.general.option_label"/>-->
<!--      </div>-->
<!--      <div class="general_line">-->
<!--        <label>"Add to cart" button text when an option is not selected</label>-->
<!--        <input type="text" v-model="proptemp.general.add_to_cart_label"/>-->
<!--      </div>-->
<!--    </div>-->
  </div>

</template>

<style scoped>

</style>