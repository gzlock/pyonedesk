import Vue from 'vue'
import Vuex from 'vuex'
import { Index } from '@/pages/index/preset'

const axios = require('axios')

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    z: 1,// windows窗口的z-index值
    activeID: null,//活跃的窗口id
    error: null,
    cache: {},// 文件夹数据缓存
    menuCallback: null,
    createWindowFromMenu: null,
  },
  mutations: {
    setError(state, response, title = '错误') {
      state.error = { title: title, content: response.data }
    },
    setCache(state, { url, res }) {
      state.cache[url] = res
      // console.log('设置缓存', state.cache)
    },
    showMenu(state, { e, id, file }) {
      state.menuCallback(e, id, file)
    },
    createWindowFromMenu(state, { file, active = false }) {
      state.createWindowFromMenu(file, active)
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
    /***
     * 有缓存
     * @param context
     * @param user
     * @param path
     * @param force
     * @returns {Promise<*>}
     */
    async load(context, { user, path, force = false }) {
      const url = Index.loadFile + '/' + user.id + '?path=' + path
      console.log('load', url, force)
      if(!!context.state.cache[url] && !force) {
        // console.log('有缓存')
        return context.state.cache[url]
      }
      const res = await axios.get(url)
      if(res.status === 200)
        context.commit('setCache', { url, res })
      return res
    },
  },
})
