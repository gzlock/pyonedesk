import Vue from 'vue'
import Vuex from 'vuex'
import { Index } from '../index/preset'
import { API } from '../admin/preset'
import { sortBy } from 'lodash'
import queue from 'async/queue'
import { FileState } from './js/file'
import { Window, WindowEvent } from './js/window'

const axios = require('axios')

Vue.use(Vuex)

const uploadQueue = queue(
  ({ user, file }, cb) => {
    const formData = new FormData(),
      url = API.uploadFile + '/' + user.id + '?type=file&path=' + file.path
    file.state = FileState.Uploading
    formData.append('file', file.file)
    axios({
        method: 'post',
        url, data: formData, headers: { 'Content-Type': 'multipart/form-data' },
      },
    ).then(res => {
      console.log('SUCCESS!!', res)
      // res.data['file']['mimeType']
      cb && cb()
    }).catch(() => {
      console.log('FAILURE!!')
      cb && cb()
    })
  }, 1)

export default new Vuex.Store({
  state: {
    z: 1,// windows窗口的z-index值
    windows: {},
    menu: { show: false, x: 0, y: 0, id: null, file: null },
    menuExtraItems: [],//右键菜单额外的项目
    activeID: null,//活跃的窗口id
    error: null,
    cache: {},// 文件夹数据缓存
    uploading: {},//上传文件队列
    uploadingLength: 0,
  },
  getters: {
    getUploading: state => (user, path, fileState = FileState.Uploading) => {
      console.log('getters getUploading', user, path, fileState)
      if(state.uploading[user.id] && state.uploading[user.id][path])
        return state.uploading[user.id][path].filter(
          file => file.state === fileState)
      return []
    },
  },
  mutations: {
    setError(state, response, title = '错误') {
      state.error = { title: title, content: response.data }
    },
    setCache(state, { url, res }) {
      state.cache[url] = res
      // console.log('设置缓存', state.cache)
    },
    createWindow(state, { user, file, active = false }) {
      console.log('createWindow')
      const win = new Window(user, file, state.z)
      Vue.set(state.windows, win.id, win)
      state.z++
      if(active)
        state.activeID = win.id
    },
    createWindowFromMenu(state, { file }) {
      this.commit('createWindow',
        { user: state.windows[state.menu.id].user, file, active: true })
    },
    /**
     * 显示文件的右键菜单
     * @param state
     * @param e
     * @param id
     * @param file
     */
    contextmenu(state, { e, id, file }) {
      console.log('右键', e, id, file)
      state.menu.show = true
      state.menu.x = e.clientX
      state.menu.y = e.clientY
      state.menu.file = file
      state.menu.id = id
    },
    /**
     * 添加额外的菜单
     * @param state
     * @param name
     * @param click
     */
    appendMenuItem(state, { name, click }) {
      state.menuExtraItems.push({ name, click })
    },
    /**
     * 关闭所有窗口
     * @param state
     */
    clearWindow(state) {
      state.windows = {}
    },
    /**
     * 关闭窗口
     * @param state
     * @param id
     */
    closeWindow(state, id) {
      state.windows[id].clearEventListener()
      Vue.delete(state.windows, id)
    },
    /**
     * 将窗口置顶，并重新梳理z
     * @param state
     * @param id
     */
    windowSetTop(state, id) {
      state.activeID = id
      state.windows[id].z = state.z
      const sorted = sortBy(state.windows, 'z')
      sorted.forEach(win => {
        const index = sorted.indexOf(win)
        win.z = index + 1
      })
      state.z = sorted.length + 1
    },
    addUploadFile(state, { id, user, path, file }) {
      if(!state.uploading[user.id])
        Vue.set(state.uploading, user.id, {})
      if(!state.uploading[user.id][path])
        Vue.set(state.uploading[user.id], path, [])
      state.uploading[user.id][path].push(file)
      file.state = FileState.Waiting
      state.uploadingLength++
      uploadQueue.push({ user, file }, () => {
        console.log('上传完成', file.path)
        state.uploadingLength--
        file.state = FileState.Normal
        state.windows[id].trigger(WindowEvent.FileUploaded, file)
      })
    },
    cancelUploadFile(state, { user, path, file }) {
      if(state.uploading[user.id] && state.uploading[user.id][path]) {
        const index = state.uploading[user.id][path].indexOf(file)
        if(index > -1) {
          state.uploading[user.id][path].splice(index, 1)
          state.uploadingLength--
        }
      }
    },
    cancelUploadByFile(state, { user, file }) {
      if(state.uploading[user.id]) {
        const paths = Object.values(state.uploading[user.id])
        for(let i = 0; i < paths.length; i++) {
          const index = paths[i].indexOf(file)
          if(index > -1) {
            paths[i].splice(index, 1)
            break
          }
        }
      }
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
