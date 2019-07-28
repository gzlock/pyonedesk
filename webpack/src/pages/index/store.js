import Vue from 'vue'
import Vuex from 'vuex'
import { Index } from '../index/preset'
import { API } from '../admin/preset'
import { findIndex, sortBy } from 'lodash'
import queue from 'async/queue'
import { FileState } from './js/file'
import { Window, WindowEvent } from './js/window'
import { join } from 'path'

const axios = require('axios')

Vue.use(Vuex)

//文件上传队列
const uploadQueue = queue(
  (data, cb) => {
    const { user, file } = data
    file.state = data.state = FileState.Uploading
    const formData = new FormData(),
      url = join(API.uploadFile, user.id) + '?type=file&path=' +
        join(file.path, file.name)
    formData.append('file', file.file)
    axios({
        method: 'post',
        url,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
      },
    ).then(({ data }) => {
      console.log('SUCCESS!!')
      file.setFromData(data)
      file.setType()
      //显示通知
      $vue.$notify.success({ title: '上传成功', message: file.name })
      cb && cb(true)
    }).catch(({ response }) => {
      console.log('FAILURE!!', response)
      file.reason = response.data
      //显示通知
      $vue.$notify.error({ title: '上传失败：' + file.name, message: file.reason })
      cb && cb(false)
    })
  }, 5)
let $vue
const $store = new Vuex.Store({
  state: {
    z: 1,// windows窗口的z-index值
    windows: {},
    menu: { show: false, x: 0, y: 0, id: null, file: null },
    menuExtraItems: [],//右键菜单额外的项目
    activeID: null,//活跃的窗口id
    error: null,
    cache: {},// 文件夹数据缓存
    uploading: [],//上传文件队列
    uploadingLength: 0,//用于阻止用户刷新网页
    uploadQueueConcurrency: uploadQueue.concurrency,
    settings: false,//是否显示全局设置
  },
  getters: {
    getUploading: state => (user, path, fileState = FileState.Uploading) => {
      /*console.log('getters getUploading', user, path, fileState,
        state.uploading.length)*/
      return state.uploading.filter(data => {
        return data.user === user && data.path === path && data.state ===
          fileState
      })
    },
    getUploadingDataByFile: state => (file) => {
      const index = findIndex(state.uploading, ['file', file])
      if(index > -1)
        return state.uploading[index]
      else
        return null
    },
    getUploadQueueConcurrency(state) {return state.uploadQueueConcurrency},
  },
  mutations: {
    setVueInstance(state, vue) {
      $vue = vue
    },
    setUploadQueueConcurrency(state, count) {
      state.uploadQueueConcurrency = count
      uploadQueue.concurrency = count
      console.log('改变后', uploadQueue.concurrency)
    },
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
    /**
     *
     * @param state
     * @param id
     * @param path
     * @param file
     */
    uploadFile(state, { id, path, file }) {
      const user = state.windows[id].user
      const data = { id, user, path, file, state: FileState.Waiting }
      this.commit('uploadQueuePush', data)
    },
    cancelUploadFile(state, file) {
      const index = findIndex(state.uploading, ['file', file])
      if(index > -1) {
        state.uploading.splice(index, 1)
        uploadQueue.remove(({ data }) => {
          // console.log('上传队列 remove', data)
          return data.file === file
        })
      }
    },
    uploadQueuePush(state, data) {
      const { id, file } = data
      const index = state.uploading.indexOf(data)
      if(index > -1)
        state.uploading.splice(index, 1)
      state.uploading.push(data)
      file.state = data.state = FileState.Waiting
      uploadQueue.push(data, result => {
        console.log('上传结果', file.path, result)
        const index = state.uploading.indexOf(data)
        if(index > -1)
          state.uploading.splice(index, 1)
        if(result) {
          //上传成功
          file.state = FileState.Normal
          state.windows[id].trigger(WindowEvent.FileUploaded, file)
        } else {
          //上传失败
          file.state = data.state = FileState.UploadFail
          state.uploading.push(data)
        }
      })
    },
    clearUploadingFile(state, fileState) {
      state.uploading = state.uploading.filter(
        ({ file }) => file.state !== fileState)
      uploadQueue.kill()
    },
    deleteCache(state, { user, path }) {
      const url = Index.loadFile + '/' + user.id + '?path=' + path
      delete state.cache[url]
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
      const url = Index.loadFile + '/' + user.id + '?path=' +
        encodeURIComponent(path)
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

export default $store
