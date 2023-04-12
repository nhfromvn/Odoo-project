import {createApp} from 'vue/dist/vue.esm-bundler';
import Shopify from './Shopify.vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {fas} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'
import {far} from '@fortawesome/free-regular-svg-icons';
import {faInstagram} from "@fortawesome/free-brands-svg-icons";

library.add(fas, far, faInstagram)

createApp(Shopify)
    .component("font-awesome-icon", FontAwesomeIcon).use(Antd)
    .mount('#app_extension')