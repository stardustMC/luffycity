import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
// import 'element-plus/dist/index.css'
import store from "./store"

import 'element-plus/theme-chalk/index.css'

createApp(App).use(router).use(store).mount('#app')
