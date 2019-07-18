<template>
    <div class="text-editor">

    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'

  export default {
    extends: WindowBaeContent,
    name: 'window-editor',
    props: ['id', 'user', 'file'],
    data() {
      return {
        $cm: null,
      }
    },
    methods: {
      async loadContent(force = false) {
        const path = ':' + this.file.path
        const { data: msData } = await this.$store.dispatch('load', { force, user: this.user, path })
        // console.log('读取文本OD数据', msData)
        const { data: txtData } = await this.$http.get(msData['@microsoft.graph.downloadUrl'])
        // console.log('读取文本', txtData)
        this.$cm.setValue(txtData.toString())
        let fileFormat = this.file.name.match(/.+\.([^.]+)$/), mode, spec
        console.log('editor 1', fileFormat)
        if(fileFormat) {
          const info = CodeMirror.findModeByExtension(fileFormat[1])
          if(info) {
            mode = info.mode
            spec = info.mime
          }
        }
        console.log('editor 2', mode, spec)
        if(mode) {
          this.$cm.setOption('mode', spec)
          CodeMirror.autoLoadMode(this.$cm, mode)
        } else {
          this.$cm.setOption('mode', 'text/plain')
        }
      },
    },
    mounted() {
      CodeMirror.modeURL = 'https://cdn.bootcss.com/codemirror/5.48.0/mode/%N/%N.js'
      this.$cm = CodeMirror(this.$el, {
        lineNumbers: true,
      })
    },
  }
</script>

<style lang="scss">
    .text-editor {
        height: 100%;

        .CodeMirror {
            width: 100%;
            height: 100%;
        }
    }
</style>