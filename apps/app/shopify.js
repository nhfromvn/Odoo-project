import {createApp, h} from 'vue/dist/vue.esm-bundler';
import Shopify from './Shopify.vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import axios from "axios";

var temp = {}
axios.post("/apps/king_variant/king_variant/show", {
    shop_url: window.location.host,
}).then((res) => {
    console.log(res.data.result)
    temp = res.data.result
    console.log(temp)
    var elements = document.getElementsByClassName('king_variant')
    if (elements) {
        for (let element of elements) {
            createApp({
                render: () => {
                    return h(Shopify, {
                        product_id: element.getAttribute('product_id'),
                        temp: temp,
                        collection: true,
                        att_product_page: null,
                    })
                }
            }).mount(element)
        }
    }
    var list_product_element = document.getElementsByClassName('king_variant_product_page')
    if (list_product_element) {
        for (let element of list_product_element) {
            createApp({
                render: () => {
                    return h(Shopify, {
                        product_id: element.getAttribute('product_id'),
                        temp: temp,
                        collection: false,
                        att_product_page: {
                            att_for: element.getAttribute('for'),
                            option_name: element.getAttribute('option_name'),
                            value: element.getAttribute('value'),
                        },
                    })
                }
            }).mount(element)
        }


    }

})

console.log(temp)
