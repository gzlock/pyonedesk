<template>
    <div @dragenter.prevent="dragEnter" @dragover.prevent
         @drop.prevent="dropFile" class="folder-container">
        <div class="upload-icon" v-if="isDragEnter" @dragleave.prevent="dragLeave" ref="dragLeave">
            <svg aria-hidden="true" class="icon">
                <use data-v-093dcf52="" xlink:href="#py_shangchuan1"></use>
            </svg>
            <div>
                将文件上传到这个文件夹<br>
                注意：通过拖拽文件夹上传有文件数量限制
            </div>
        </div>
        <!--正常文件-->
        <div class="folder">
            <file-icon v-for="(file,i) in files" :key="i" :file="file" @dblclick="open" :id="id"/>
        </div>

        <!--上传队列-->
        <div class="top-border" v-if="uploading.length > 0">
            <div class="header">上传中</div>
            <div class="folder">
                <file-icon v-for="(file,i) in uploading" :key="i" :file="file" :id="id"/>
            </div>
        </div>
        <div class="top-border" v-if="waiting.length > 0">
            <div class="header">等候上传</div>
            <div class="folder">
                <file-icon v-for="(file,i) in waiting" :key="i" :file="file" :id="id"
                           @cancelUpload="cancelUpload"/>
            </div>
        </div>
        <input type="file" style="display: none" class="hidden-file-input" multiple ref="fileInput"
               @change="selectUploadFiles"/>
    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'
  import { join } from 'path'
  import FileIcon from './file-icon'
  import { File, FileState, FileType } from '../js/file'
  import { WindowEvent } from '../js/window'

  async function traverseFileTree(file, path) {
    path = path || ''
    const files = []
    if(file.isFile) {
      // Get file
      await new Promise(resolve => {
        file.file(f => {
          const file = new File(f.name, path + f.name, f.type)
          file.file = f
          files.push(file)
          resolve()
        })
      })
    } else if(file.isDirectory) {
      // Get folder contents
      await new Promise(resolve => {
        file.createReader().readEntries(async entries => {
          for(let i = 0; i < entries.length; i++) {
            files.push(...await traverseFileTree(entries[i], path + file.name + '/'))
          }
          resolve()
        })
      })
    }
    return files
  }

  export default {
    extends: WindowBaeContent,
    name: 'window-folder',
    components: { FileIcon },
    props: ['id', 'user', 'file'],
    data() {
      return {
        loading: false,
        isDragEnter: false,
        files: [],
      }
    },
    watch: {
      file() {
        this.files.length = 0
        this.load()
      },
    },
    computed: {
      uploading() {
        return this.$store.getters.getUploading(this.user, this.file.path)
      },
      waiting() {
        return this.$store.getters.getUploading(this.user, this.file.path, FileState.Waiting)
      },
    },
    methods: {
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
        const path = this.file.path === '/' ? this.file.path : this.file.path + '/'
        const files = e.target.files
        for(let i = 0; i < files.length; i++) {
          const file = files[i]
          console.log('input file', file)
          const _file = new File(file.name, path + file.webkitRelativePath + file.name, file.type)
          _file.file = file
          this.$store.commit('addUploadFile', { id: this.id, user: this.user, path: this.file.path, file: _file })
        }
      },
      async dropFile(e) {
        //通过 拖文件 上传文件
        this.isDragEnter = false
        const path = this.file.path === '/' ? this.file.path : this.file.path + '/'
        const items = e.dataTransfer.items, files = []
        for(let i = 0; i < items.length; i++) {
          const item = items[i].webkitGetAsEntry()
          if(item)
            files.push(...await traverseFileTree(item))
        }
        console.log('拖拽文件', items.length, files.length)
        files.forEach(file => {
          file.path = path + file.path
          this.$store.commit('addUploadFile', { id: this.id, user: this.user, path: this.file.path, file })
        })
      },
      open(file) {
        this.$emit('open', file)
      },
      async loadContent(force = false) {
        //清空 上传列表
        let path = ''
        if(this.file.path !== '/')
          path = `:${this.file.path}:`
        path += '/children?expand=thumbnails'

        const { data } = await this.$store.dispatch('load', { user: this.user, path, force })
        this.files = data.value.map(file => {
          const path = join(this.file.path, file.name)
          const mimeType = file.file ? file.file.mimeType : null
          const _file = new File(file.name, path, mimeType)
          if(_file.type === FileType.Image)
            _file.thumbnail = file.thumbnails[0]['small']['url']
          return _file
        })
      },
      cancelUpload(file) {
        this.$store.commit('cancelUploadFile', { user: this.user, path: this.file.path, file })
      },
      removeFile(file) {
        const index = this.files.indexOf(file)
        if(index > -1)
          this.files.splice(index, 1)
      },
      fileUploaded(file) {
        this.files.push(file)
      },
    },
    mounted() {
      this.$store.state.windows[this.id].addEventListener(WindowEvent.FileUploaded, this.fileUploaded)
      this.$store.state.windows[this.id].addEventListener(WindowEvent.FileDeleted, this.removeFile)
    },
    beforeDestroy() {
      if(this.$store.state.windows[this.id]) {
        this.$store.state.windows[this.id].removeEventListener(WindowEvent.FileUploaded, this.fileUploaded)
        this.$store.state.windows[this.id].removeEventListener(WindowEvent.FileDeleted, this.removeFile)
      }
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