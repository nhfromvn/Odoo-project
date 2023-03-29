<template>
  <div class="container" id="container">
    <div class="d-flex justify-content-center">
      <div id="frame_427319039">
        <button class="head_btn" id="add_product">Add Product</button>
        <button class="head_btn" id="customization">Customization</button>
        <button class="head_btn" id="installation">Installation</button>
      </div>
    </div>
    <div class="d-flex justify-content-end">
      <div class="right_top_btns" style="display: flex; gap: 19px">
        <button id="btn_cancel">
          Cancel
        </button>
        <button id="btn_save" @click="save()">
          SAVE
        </button>
      </div>
    </div>
    <div id="enable_widget">
      <p>
        Enable Widget
      </p>
      <a-switch v-model:checked="checked1" checked-children="ON" un-checked-children="OFF"/>
    </div>

    <div id="recommend_text" class="align-items-center">
      <p class="d-flex align-content-center">Manual Recommendation</p>
      <font-awesome-icon :icon="['fas', 'circle-question']"/>
    </div>
    <div style="position: relative">
      <div v-if="!checked1" class="blur"></div>
      <div id="rectangle_34624168">
        <div id="choose_text" class="d-flex align-items-center justify-items-center">
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>Choose recommendation product(s)</p>
        </div>
        <a-input id="search_recommend_bar" v-model:value="search_recommendation" placeholder="Search product by name"
                 onkeyup="showSuggestion()"
                 :suffix="this.list_recommend_product.length + ' selected'"/>
        <div class="show_product" v-if="this.list_recommend_product.length > 0">
          <div class="product" v-for="product in this.list_recommend_product" :key="product">
            <p>
              {{ product.name }}
            </p>
            <font-awesome-icon :icon="['fas', 'circle-xmark']" size="sm"
                               @click="handleClickRecommendProduct(product.id)"
                               style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"/>
          </div>
        </div>
        <table class="table table-responsive table-bordered" id="table_recommend">
          <thead>
          <tr>
            <th>
              <div>
                <input type="checkbox" v-model="check_all_recommend" @change="handleCheckAllRecommend()">
              </div>
            </th>
            <th>Image</th>
            <th>Product Name</th>
            <th>Price</th>
            <th>Compare At Price</th>
            <th>In Stock</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="product in filteredRowsRecommend">
            <td>
              <div>
                <input type="checkbox" v-model="product.check_recommend">
              </div>
            </td>
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
          </tr>
          </tbody>
        </table>
      </div>
      <div id="rectangle_34624142">
        <div id="choose_text" class="d-flex align-items-center justify-items-center">
          <font-awesome-icon :icon="['fas', 'circle-question']"/>
          <p>Choose exclude product(s)</p>
        </div>
        <a-input id="search_exclude_bar" v-model:value="search_exclude" placeholder="Search product by name"
                 :suffix="this.list_exclude_product.length + ' selected'"/>
        <div class="show_product" v-if="this.list_exclude_product.length > 0">
          <div class="product" v-for="product in this.list_exclude_product" :key="product">
            <p>
              {{ product.name }}
            </p>
            <font-awesome-icon :icon="['fas', 'circle-xmark']" size="sm"
                               @click="handleClickExcludeProduct(product.id)"
                               style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"/>
          </div>
        </div>
        <table class="table table-responsive table-bordered" id="table_exclude">
          <thead>
          <tr>
            <th>
              <div>
                <input type="checkbox" v-model="check_all_exclude" @change="handleCheckAllExclude()">
              </div>
            </th>
            <th>Image</th>
            <th>Product Name</th>
            <th>Price</th>
            <th>Compare At Price</th>
            <th>In Stock</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="product in filteredRowsExclude">
            <td>
              <div>
                <input type="checkbox" v-model="product.check_exclude"></div>
            </td>
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.name }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, reactive, toRefs, h} from 'vue';
import {notification} from 'ant-design-vue';
import {CloseCircleFilled} from '@ant-design/icons-vue'

export default {
  name: "AddProduct",
  watch: {
    list_recommend_product: function () {
      this.check_all_recommend = this.list_recommend_product.length == this.filteredRowsRecommend.length
    },
    list_exclude_product: function () {
      this.check_all_exclude = this.list_exclude_product.length == this.filteredRowsExclude.length
    }
  },
  computed: {
    // notification(){
    //    if(this.list_recommend_product>5){
    //      return this.openNotification()
    //    }
    //  },
    list_recommend_product: function () {
      return this.list_product.filter(product => product.check_recommend == true)
    },
    list_exclude_product: function () {
      return this.list_product.filter(product => product.check_exclude == true)
    },
    filteredRowsRecommend: function () {
      var self = this;
      return this.list_product.filter(function (product) {
        return String(product.name).toLowerCase().indexOf(self.search_recommendation.toLowerCase()) > -1
      })
    },
    filteredRowsExclude: function () {
      var self = this;
      return this.list_product.filter(function (product) {
        return String(product.name).toLowerCase().indexOf(self.search_exclude.toLowerCase()) > -1
      })
    }
  }
  ,
  setup() {
    const state = reactive({
      checked1: true
    });
    const openNotification = () => {
      notification.open({
        message: 'Notification Title',
        description:
            'This is the content of the notification. This is the content of the notification. This is the content of the notification.',
        onClick: () => {
          console.log('Notification Clicked!');
        },
        duration: 3
      });
    };
    return {
      openNotification, ...toRefs(state)
    };
  },
  methods: {
    handleCheckAllRecommend() {
      if (this.check_all_recommend) {
        this.list_product.filter(product => product.check_recommend = true)
      } else {
        this.list_product.filter(product => product.check_recommend = false)
      }
    },
    handleCheckAllExclude() {
      if (this.check_all_exclude) {
        this.list_product.filter(product => product.check_exclude = true)
      } else {
        this.list_product.filter(product => product.check_exclude = false)

      }
    },
    handleClickRecommendProduct(id) {
      this.list_product.find(product => product.id == id).check_recommend = false
    },
    handleClickExcludeProduct(id) {
      this.list_product.find(product => product.id == id).check_exclude = false
    },
    show_toast: function (type, message, description, duration) {
      notification[type]({
        description: description,
        message: message,
        duration: duration,
        class: 'error_popup',
        closeIcon: function (e) {
          return (<CloseCircleFilled/>)
        }
      })
    },
    save() {
      if (this.list_recommend_product.length > 5||this.list_exclude_product.length > 5) {
        this.show_toast(
            'open',
            'You have reach the product limitation.',
            'Please untick any products from the list to continue selecting.',
            3
        )
      }
    }
  },
  data() {
    return {
      list_product: [{
        check_recommend: false,
        check_exclude: false,
        id: 0,
        name: 'giay',

      }, {
        check_recommend: false,
        check_exclude: false,
        id: 1,
        name: 'quan',

      }, {
        check_recommend: false,
        check_exclude: false,
        id: 2,
        name: 'ao',

      }, {
        check_recommend: false,
        check_exclude: false,
        id: 3,
        name: 'mu',

      }, {
        check_recommend: false,
        check_exclude: false,
        id: 4,
        name: 'kinh',

      },
        {
          check_recommend: false,
          check_exclude: false,
          id: 5,
          name: 'dong_ho',

        }
      ],
      search_recommendation: '',
      check_all_recommend: false,
      search_exclude: '',
      check_all_exclude: false,
    }
  },

}
// axios.get("/shopify/sync/product").then((res) => {
//     this.list_product = res.data.products
// })
</script>

<style scoped>
#container {
  /*top: 100px;*/
}

#frame_427319039 {
  /*position: fixed;*/
}

#add_product {
  box-sizing: border-box;

  /* Auto layout */

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 6px 16px;
  width: 184.67px;
  height: 36px;
  background: #FFFFFF;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.25);
}

.right_top_btns {
  width: 200px;
  margin-bottom: 0px;
}

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

#enable_widget {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
}

#enable_widget p {
  margin-bottom: 0px !important;
  width: 127px;
  height: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 18px;
  line-height: 22px;
  /* identical to box height, or 122% */
  color: #000000;
}

#recommend_text {
  display: flex;
}

#recommend_text svg {
  width: 12px;
  height: 12px;
}

#recommend_text p {
  padding-right: 5px;
  height: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 22px;
  color: #000000;
  margin-bottom: 0px !important;
}

#choose_text svg {
  width: 12px;
  height: 12px;
}

#choose_text p {
  width: 660px;
  height: 28px;
  padding-left: 5px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-size: 18px;
  line-height: 28px;
  /* identical to box height, or 156% */
  display: flex;
  align-items: center;
  /* Text/Default */
  color: #202223;
  margin-bottom: 0px !important;
}

#rectangle_34624168 {
  box-sizing: border-box;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  margin-bottom: 10px;
  padding: 10px;
}

#rectangle_34624142 {
  box-sizing: border-box;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  padding: 10px;
}

#table_recommend {

}

#table_exclude {

}

#search_recommend_bar {

  box-sizing: border-box;
  width: 1064px;
  height: 40px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

#search_exclude_bar {

  box-sizing: border-box;
  width: 1064px;
  height: 40px;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
}

.show_product {
  display: flex;

}

.product {
  display: flex;
  align-items: center;
  box-sizing: border-box;
  background: #FFFFFF;
  border: 1px solid #E2E2E2;
  border-radius: 6px;
  gap: 5px;
}

.product path {
  border-radius: 50%;
  width: 15px;
  height: 15px;
}

.blur {
  height: 100%;
  width: 100%;
  z-index: 100;
  opacity: 0.5;
  position: absolute;
  top: 0;
  left: 0;
  background-color: #FFFFFF;
}
</style>