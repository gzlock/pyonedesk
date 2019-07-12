import Vue from 'vue'
import Vuex from 'vuex'

const axios = require('axios')

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    accounts: {},
    error: null,
    isMobile: document.body.clientWidth < 700,
    labelPosition: document.body.clientWidth < 700 ? 'top' : 'right',
  },
  mutations: {
    setAccounts(state, accounts) {
      state.accounts = accounts
    },
    updateDefaultAccount(state, id) {
      Object.values(state.accounts).forEach(account => {
        account.default = account.id === id
      })
    },
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
