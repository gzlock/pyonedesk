<template>
    <div class="folder" @dragover.prevent @drop.prevent="drop">
        <file-icon v-for="(file,i) in files" :key="i" :file="file"
                   @dblclick="open" :id="id"/>
    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'
  import { join } from 'path'
  import FileIcon from './file-icon'
  import { File, FileType } from '../js/file'

  export default {
    extends: WindowBaeContent,
    name: 'window-folder',
    components: { FileIcon },
    props: ['user', 'file', 'id'],
    data() {
      return {
        loading: false,
        files: [],
        uploads: [],
      }
    },
    watch: { file() {this.load()} },
    methods: {
      drop(ev) {
        console.log('drop', ev)
        if(ev.dataTransfer.items) {
          // Use DataTransferItemList interface to access the file(s)
          for(let i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if(ev.dataTransfer.items[i].kind === 'file') {
              const file = ev.dataTransfer.items[i].getAsFile()
              console.log('1 ... file[' + i + '].name = ' + file.name)
            }
          }
        } else {
          // Use DataTransfer interface to access the file(s)
          for(let i = 0; i < ev.dataTransfer.files.length; i++) {
            console.log('2 ... file[' + i + '].name = ' + ev.dataTransfer.files[i].name)
          }
        }
      },
      open(file) {
        this.$emit('open', file)
      },
      async loadContent(force = false) {
        //清空 上传列表
        this.uploads.length = 0
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
    },
  }
</script>

<style scoped lang="scss">

    .folder {
        user-select: none;
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
        justify-content: flex-start;

        .file {
            margin: 10px 0 0 10px;
        }
    }
</style>