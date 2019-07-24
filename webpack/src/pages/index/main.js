import Vue from 'vue'
import App from './App.vue'
import store from './store'
import '@/assets/global.scss'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.prototype.$http = require('axios')


new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
