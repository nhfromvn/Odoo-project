import {createApp, h} from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
// import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import 'bootstrap'

var app = createApp({
    name: 'App',
    render: () => {
        return <App/>
    }
})
// app.use(Antd)
app.mount('#app')