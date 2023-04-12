<template>
  <div class="container" id="container">
    <div id="text_welcome">Welcome, Hoang Nam!</div>
    <div>
      <table class="table table-responsive table-bordered" id="table_1">
        <tr>
          <th>
            #
          </th>
          <th>
            Widget Title
          </th>
          <th>
            Widget Description
          </th>
          <th>
            Product included
          </th>
          <th>
            Total Price
          </th>
          <th>
            Status
          </th>
        </tr>
        <tr>
          <td>
            1
          </td>
          <td>
            {{ proptemp.widget_title }}
          </td>
          <td>
            {{ proptemp.widget_description }}
          </td>
          <td>
            {{ proptemp.product_included }}
          </td>
          <td>
            ${{ proptemp.total_price }}
          </td>
          <td>
            <div class="align-items-center">
              <a-switch @change="changeStatus" v-model:checked="this.status" checked-children="ON"
                        un-checked-children="OFF"/>
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
  <div id="test"></div>
</template>

<script>
import {reactive, toRefs} from 'vue';
import axios from "axios";

export default {
  emits: ['sendStatus'],
  name: "Dashboard",
  props: {
    proptemp: Object
  },
  mounted() {
    let self = this
    axios.get("/bought-together/get/widget").then((res) => {
      self.status = res.data.status
      self.shop = res.data.shop
      console.log(self.status)
    })
    console.log(this.proptemp)
  },
  data() {
    return {
      shop:'',
      status: false
    }
  },
  methods: {
    changeStatus() {
      let self = this
      axios.post('/bought-together/save/status', {
        shop_url: self.shop
        , status: self.status
      }).then((res) => {
        if (res.data.result.status) {
          console.log(res)
          window.location.reload()
          alert('Save Success')
        }
      });
      console.log(this.status)
      this.$emit('sendStatus', this.status)

    }
  },
  setup() {
    const state = reactive({
      checked1: true
    });

    function test() {
      console.log(state.checked1)
    }

    return {
      ...toRefs(state),
      test
    };
  },
}
</script>

<style scoped>
#test {
  height: 1000px;
  background-color: #000000;
}

.container {
  padding: 57px;
  width: 100%;
}

#text_welcome {
  padding: 20px 20px 20px 20px;
  width: 500px;
  height: 100px;
  left: 20px;
  top: 5px;
  font-family: 'Kanit';
  font-style: normal;
  font-weight: 600;
  font-size: 27px;
  line-height: 24px;
  color: #000000;
}

#table_1 {
  display: table;
  width: 100%;
  left: 20px;
  top: 5px;
  column-gap: 30px;
  row-gap: 30px;
}


#table_1 th {
  text-align: left !important;
}

#table_1 td {
  text-align: left;
  font-family: 'Inter';
  font-style: normal;
  color: rgba(0, 0, 0, 0.85);
  flex: none;
  order: 0;
  flex-grow: 0;
}

</style>