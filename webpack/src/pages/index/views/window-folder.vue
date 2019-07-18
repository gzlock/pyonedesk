<template>
    <div class="folder">
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
      }
    },
    watch: { file() {this.load()} },
    methods: {
      open(file) {
        this.$emit('open', file)
      },
      async loadContent(force = false) {
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