<template>
  <div id="content_right">
    <div id="rectangle_widget" style="justify-content: center">
      <div id="show_widget_title"
           :style="{
                    color: widget_title_color,
                fontSize: widget_title_font_size.value+'px'
                    }"
      >{{ widget_title }}{{ widget_title_font_size.value }}
      </div>
      <div id="show_widget_description"
           :style="{
                    color: widget_description_color,
                    fontSize : widget_description_font_size.value+'px'
                    }">{{ widget_description }}{{ widget_description_font_size.value }}
      </div>
      <div style="display: flex;
                      justify-content: space-around">
        <div id="images">
          <div v-for="product in list_recommend_product">
            <div style="display: flex" v-if="list_recommend_product.indexOf(product)<numbers_product">
              <img style="width: 65px;
                        height: 61px;" :src="product.image_url"/>
              <div style="padding: 9px"
                   v-if="list_recommend_product.indexOf(product)!=numbers_product-1&&list_recommend_product.indexOf(product)!=list_recommend_product.length-1"
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
          <button @click="add_to_cart" id="show_button" :style="{color: widget_button_text_color,
                                                backgroundColor:  widget_button_bg_color,
                                                borderColor: widget_button_border_color}">
            {{ widget_button_text }}
          </button>
        </div>
      </div>
      <div v-for="product in list_recommend_product">
        <div class="products" v-if="list_recommend_product.indexOf(product)<numbers_product">
          <div style="display: flex;
                        gap:14px">
            <input type="checkbox" v-model="product.check_box">
            <p>{{ product.check_box }}</p>
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
</template>

<script>
import axios from 'axios'

export default {
  name: "App_extension",
  methods: {
    add_to_cart() {
      if (this.items.length > 0) {
        let formData = {
          'items': this.items
        }
        console.log(this.items)
        axios.post(`${window.Shopify.routes.root}cart/add.js`, formData, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
            .then(response => {
              console.log(response.data);
              window.location.replace(window.Shopify.routes.root + 'cart');
            })
            .catch(error => {
              console.error('Error:', error);
            });
      } else {
        alert('chua chon san pham')
      }
    }
  },
  computed: {
    items: function () {
      let items = []
      for (let product of this.list_recommend_product) {
        if (product.check_box) {
          items.push({
            'id': Number(product.variant_id),
            'quantity': 1
          })
        }
      }
      return items
    },
    total_price: function () {
      let price = 0
      for (let product of this.list_recommend_product) {
        price += Number(product.price)
      }
      return price
    }
    ,
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
  },
  data() {
    return {
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
      list_recommend_product: [],
      list_exclude_product: [],
      widget_title: '',
      widget_title_color: '',
      widget_title_font_size: {
        name: 'Medium',
        value: 18
      },
      widget_description: '',
      widget_description_color: '',
      widget_description_font_size: {
        name: 'Medium',
        value: 18
      },
      widget_button_text: '',
      widget_button_text_color: '',
      widget_button_bg_color: '',
      widget_button_border_color: '',
      numbers_product: 0,
      product_included: 0,
    }
  },
  mounted() {
    let self = this
    console.log(window.location)
    axios.post("/apps/bought-together/bought-together/show/widget", {shop_url: window.location.host}).then((res) => {
      console.log(res)
      let widget = res.data.result
      self.widget_title = widget.widget_title
      self.widget_title_color = widget.widget_title_color
      self.widget_title_font_size = self.font_sizes.find(font => font.name.toLowerCase() == widget.widget_title_font_size)
      self.widget_description = widget.widget_description
      self.widget_description_color = widget.widget_description_color
      self.widget_description_font_size = self.font_sizes.find(font => font.name.toLowerCase() == widget.widget_description_font_size)
      self.widget_button_text = widget.widget_button_text
      self.widget_button_text_color = widget.widget_button_text_color
      self.widget_button_bg_color = widget.widget_button_bg_color
      self.widget_button_border_color = widget.widget_button_border_color
      self.numbers_product = widget.numbers_product
      self.product_included = widget.product_included
      self.list_recommend_product = widget.list_recommend_product
      self.list_exclude_product = widget.list_exclude_product
      for (let product of self.list_recommend_product) {
        product.check_box = false
      }
      console.log(self.widget_description_font_size.value)
      console.log(self.widget_title_font_size.value)
    })
  },

}

</script>
<style>

#show_widget_title {
  height: 24px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  line-height: 22px;
  /* or 110% */
  text-align: center;
  margin-bottom: 26px;
}

#show_widget_description {
  height: 25px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  line-height: 22px;
  /* or 157% */
  text-align: center;
  margin-bottom: 26px;
}

#images {
  display: flex;
  margin-bottom: 30px;
}

#rectangle_widget {
  box-sizing: border-box;
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
  display: flex;
  margin-bottom: 0px !important;
  text-align: center;
}

</style>