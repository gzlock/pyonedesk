import Vue from 'vue'
import App from './App.vue'
import store from './store'
import '@/assets/global.scss'

Vue.config.productionTip = false

Vue.prototype.$http = require('axios')

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
