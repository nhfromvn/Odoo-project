<script>
import {defineComponent} from 'vue'

import CollectionPage from "./components/CollectionPage.vue";
import ProductPage from "./components/ProductPage.vue";

export default defineComponent({
  name: "Shopify",
  components: {ProductPage, CollectionPage},
  props: {
    product_id: Number,
    temp: Object,
    collection: Boolean,
    att_product_page: Object,
  },
})
</script>

<template>
  <CollectionPage v-if="collection" :product_id="product_id" :temp="temp"/>
  <ProductPage v-else :att_product_page="att_product_page" :temp="temp" :product_id="product_id"/>
</template>
<style scoped>

</style>