import Vue from 'vue'
import Vuex from 'vuex'

const axios = require('axios')

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    error: null,
  },
  mutations: {
    setError(state, response, title = '错误') {
      state.error = { title: title, content: response.data }
    },
  },
  actions: {
    async api(context, data) {
      try {
        return await axios(data)
      } catch(e) {
        //
        context.commit('setError', e.response)
        return null
      }
    },
  },
})
