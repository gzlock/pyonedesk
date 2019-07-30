<template>
    <div @dragenter.prevent="dragEnter" @dragover.prevent
         @drop.prevent="dropFile" class="folder-container"
         @paste.prevent="paste">
        <div class="upload-icon" v-if="isDragEnter" @dragleave.prevent="dragLeave" ref="dragLeave">
            <svg aria-hidden="true" class="icon">
                <use data-v-093dcf52="" xlink:href="#py_shangchuan1"></use>
            </svg>
            <div>
                将文件 / 文件夹 上传到这个目录<br>
            </div>
        </div>

        <!--正常文件-->
        <div class="folder">
            <file-view v-for="(_file,i) in files" :key="i" :parent="file" :file="_file" :id="window.id"
                       @dblclick="open"/>
        </div>
        <div v-if="nextPage" class="next-page">
            <el-button @click="loadNextPage" type="text" :loading="loading">加载更多</el-button>
        </div>

        <!--上传中-->
        <div class="top-border" v-if="uploading.length > 0">
            <div class="header">
                <span>上传中，同时上传：{{queueConcurrency}}</span>
                <el-button type="text" @click="$store.state.settings=true">设置</el-button>
            </div>
            <div class="folder">
                <file-view v-for="(item,i) in uploading" :key="i" :parent="file" :file="item.file" :id="window.id"/>
            </div>
        </div>
        <!--上传失败-->
        <div class="top-border" v-if="uploadFails.length > 0">
            <div class="header">上传失败
                <el-button type="text" @click="clearUploadFail">清空</el-button>
            </div>
            <div class="folder">
                <file-view v-for="(item,i) in uploadFails" :key="i" :parent="file" :file="item.file" :id="window.id"/>
            </div>
        </div>
        <!--等待上传-->
        <div class="top-border" v-if="waiting.length > 0">
            <div class="header">等候上传
                <el-button type="text" @click="clearWaiting">全部取消</el-button>
            </div>
            <div class="folder">
                <file-view v-for="(item,i) in waiting" :key="i" :parent="file" :file="item.file" :id="window.id"/>
            </div>
        </div>
        <input type="file" style="display: none" class="hidden-file-input" multiple ref="fileInput"
               @change="selectUploadFiles"/>
    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'
  import FileView from './file'
  import { defaultSort, File, FileSortType, FileState, FileType } from '../js/file'
  import { Window, WindowEvent } from '../js/window'
  import { findIndex } from 'lodash'
  import { getFilesFromDataTransferItems } from 'datatransfer-files-promise'
  import { API } from '../../admin/preset'

  const path = require('path')

  export default {
    extends: WindowBaeContent,
    name: 'window-folder',
    components: { FileView },
    props: { window: Window, file: File },
    data() {
      return {
        isDragEnter: false,
        files: [],
        nextPage: null,
        search: '',
        sort: JSON.parse(JSON.stringify(defaultSort)),
      }
    },
    watch: {
      file() {
        this.nextPage = null
        this.files.length = 0
        this.search = ''
        this.sort = JSON.parse(JSON.stringify(defaultSort))
        this.load()
      },
    },
    computed: {
      uploading() {
        return this.$store.getters.getUploading(this.window.user, this.file.path)
      },
      waiting() {
        return this.$store.getters.getUploading(this.window.user, this.file.path, FileState.Waiting)
      },
      uploadFails() {
        return this.$store.getters.getUploading(this.window.user, this.file.path, FileState.UploadFail)
      },
      queueConcurrency: {
        get: function() {
          return this.$store.getters.getUploadQueueConcurrency
        },
        set: function(value) {
          console.log('改变队列数量', value)
          this.$store.commit('setUploadQueueConcurrency', value)
        },
      },
    },
    methods: {
      paste(e) {
        console.log('粘贴事件', e)
        const clipboardData = (e.clipboardData || e.originalEvent.clipboardData)
        if(clipboardData.items) {
          console.log('粘贴板有内容', clipboardData.items.length)
        }
      },
      dragEnter() {
        // console.log('dragEnter', e.target)
        if(this.isDragEnter)
          return
        this.isDragEnter = true
      },
      dragLeave(e) {
        // console.log('dragLeave', e.target)
        if(e.target === this.$refs.dragLeave)
          this.isDragEnter = false
      },
      click_upload(type) {
        const $input = this.$refs.fileInput
        if(type === 'folder') {
          $input.setAttribute('webkitdirectory', '')
          $input.setAttribute('directory', '')
        } else {
          $input.removeAttribute('webkitdirectory')
          $input.removeAttribute('directory')
        }
        this.$refs.fileInput.click()
      },
      selectUploadFiles(e) {
        //通过 按钮 上传文件
        const files = e.target.files
        for(let i = 0; i < files.length; i++) {
          const data = files[i]
          const _path = path.join(this.file.path, this.file.name, data.webkitRelativePath)
          console.log('input file', data)
          const file = new File(data.name, _path, data.type)
          file.file = data

          const index = findIndex(this.files, { path: data.path, name: data.name })
          if(index > -1) {
            this.$confirm(`${data.name} 已经存在，是否覆盖？`).then(() => {
              this.$store.commit('uploadFile', { id: this.window.id, path: this.file.path, file })
            }).catch(() => {})
          }
          this.$store.commit('uploadFile', { id: this.window.id, path: this.file.path, file })
        }
      },
      /**
       * 通过 拖拽 上传文件
       * @param e
       * @returns {Promise<void>}
       */
      async dropFile(e) {
        this.isDragEnter = false
        const files = await getFilesFromDataTransferItems(e.dataTransfer.items)
        files.forEach(data => {
          const split = data.filepath.split('/')
          split.pop()
          const _path = path.join(this.file.path, this.file.name, ...split),
            file = new File(data.name, _path, data.type)
          // console.log('drop file path', this.file.path, _path)
          //文件数据
          file.file = data
          // console.log('drop file 新文件', file)
          const index = findIndex(this.files, { path: file.path, name: file.name })
          if(index > -1) {
            this.$confirm(`${file.name} 已经存在，是否覆盖？`).then(() => {
              this.$store.commit('uploadFile', { id: this.window.id, path: this.file.path, file })
            }).catch(() => {})
          } else
            this.$store.commit('uploadFile', { id: this.window.id, path: this.file.path, file })
        })
      },
      open(file) {
        console.log('window-folder open', file)
        this.$emit('open', file)
      },
      async loadContent(force = false) {
        //清空 上传列表
        let _path = path.join(this.file.path, this.file.name)
        if(_path === '/')
          _path = ''
        else
          _path = `:${_path}:`
        if(this.search)
          _path += `/search(q='${this.search}')?expand=thumbnails`
        else
          _path += '/children?expand=thumbnails'

        let order = 'name'
        switch(this.sort.type) {
          case FileSortType.Name:
            order = 'name'
            break
          case FileSortType.Size:
            order = 'size'
            break
          case FileSortType.CreatedTime:
            order = 'createdDateTime'
            break
          case FileSortType.ModifiedTime:
            order = 'lastModifiedDateTime'
        }
        _path += '&orderby=' + order + ' ' + (this.sort.isUp ? 'desc' : 'asc')

        if(force)
          this.nextPage = null

        try {
          const { data } = await this.$store.dispatch('load', { user: this.window.user, path: _path, force })
          this.files = data.value.map(data => {
            const _path = path.join(this.file.path, this.file.name)
            const file = new File(data.name, _path).setFromData(data)
            return file.setFromData(data).setType().setState(FileState.Normal)
          })
          if(data['@odata.nextLink'])
            this.nextPage = data['@odata.nextLink'].split('/root')[1]
          else
            this.nextPage = null
        } catch(e) {
          console.log('folder loadContent', e)
          this.$emit('loadError', e.response.data)
        }
      },
      async loadNextPage() {
        this.loading = true
        const { data } = await this.$store.dispatch('load',
          { user: this.window.user, path: this.nextPage, force: true })
        this.files.push(...data.value.map(data => {
          const _path = path.join(this.file.path, this.file.name)
          const file = new File(data.name, _path)
          return file.setFromData(data).setType().setState(FileState.Normal)
        }))
        if(data['@odata.nextLink'])
          this.nextPage = data['@odata.nextLink'].split('/root')[1]
        else
          this.nextPage = null
        this.loading = false
      },
      removeFile(file) {
        const index = this.files.indexOf(file)
        if(index > -1)
          this.files.splice(index, 1)
      },
      fileUploaded(file) {
        //不属于这个文件夹
        if(file.path !== path.join(this.file.path, this.file.name))
          return

        const index = findIndex(this.files, { name: file.name })
        if(index > -1)
          this.files.splice(index, 1)

        this.files.push(file)
      },
      clearWaiting() {
        this.$confirm('确认清空等待上传的任务？').then(() => {
          this.$store.commit('clearUploadingFile', FileState.Waiting)
        }).catch(() => {})
      },
      clearUploadFail() {
        this.$confirm('确认清空上传失败的任务？').then(() => {
          this.$store.commit('clearUploadingFile', FileState.UploadFail)
        }).catch(() => {})
      },
      create(type, name) {
        console.log('创建', type, name)
        if(type === FileType.Folder) {
          const _path = path.join(this.file.path, this.file.name) === '/' ? '/root' : '/items/' + this.file.id
          this.$http.get(API.createFolder + '/' + this.window.user.id + '?path=' + _path + '&name=' + name).
            then(({ data }) => {
              this.files.push(
                new File(name, path.join(this.file.path, name)).setFromData(data).
                  setType(FileType.Folder).
                  setState(FileState.Normal))
            }).catch(() => {})
        } else {
          this.$alert('尚未实现')
        }
      },
      sortFile({ type, isUp }) {
        console.log('排序', type, isUp)
        this.sort.type = type
        this.sort.isUp = isUp
        this.load()
      },
      searchFile(word) {
        this.search = word
        this.load()
      },
    },
    mounted() {
      this.window.addEventListener(WindowEvent.FileUploaded, this.fileUploaded)
      this.window.addEventListener(WindowEvent.FileDeleted, this.removeFile)
      this.window.addEventListener(WindowEvent.SortFile, this.sortFile)
      this.window.addEventListener(WindowEvent.SearchFile, this.searchFile)
    },
    beforeDestroy() {
      this.window.removeEventListener(WindowEvent.FileUploaded, this.fileUploaded)
      this.window.removeEventListener(WindowEvent.FileDeleted, this.removeFile)
      this.window.removeEventListener(WindowEvent.SortFile, this.sortFile)
      this.window.removeEventListener(WindowEvent.SearchFile, this.searchFile)
    },
  }
</script>

<style scoped lang="scss">
    .folder-container {
        height: 100%;
        position: relative;


        .upload-icon {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;

            svg {
                width: 50px;
                margin-right: 20px;
                fill: blue;
            }
        }

        .next-page {
            text-align: center
        }

        .folder {
            user-select: none;
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            justify-content: flex-start;
            margin-bottom: 10px;

            .file {
                margin: 10px 0 0 10px;
            }
        }
    }

    .top-border {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #D3DCE6;

        .header {
            font-size: 14px;
            margin-left: 10px;
        }
    }


</style>