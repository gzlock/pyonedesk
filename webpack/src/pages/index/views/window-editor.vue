<template>
    <div class="text-editor-container">
        <div class="text-editor">

        </div>
        <div class="saving" :class="{show:saving}">保存中</div>
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
        saving: false,
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
      /**
       * 删除这个文件的缓存
       */
      deleteCache() {
        this.$store.commit('deleteCache', { user: this.user, path: ':' + this.file.path })
      },
      save() {
        if(this.loading || this.saving)
          return

        this.saving = true
        this.$http({
          method: 'post',
          url: '/admin/api/upload/' + this.user.id,
          params: { path: this.file.path, type: 'text' },
          data: this.$cm.getValue(),
        }).then(() => {
          this.deleteCache()
        }).catch(err => {
          this.$notify.error(`${this.file.name} 保存失败：${err.response.data}`)
        }).finally(() => {
          this.saving = false
        })
      },
    },
    mounted() {
      CodeMirror.modeURL = 'https://cdn.bootcss.com/codemirror/5.48.0/mode/%N/%N.js'
      this.$cm = CodeMirror(this.$el.querySelector('.text-editor'), {
        lineNumbers: true,
        extraKeys: {
          'Ctrl-S': this.save,
          'Cmd-S': this.save,
        },
      })
    },
  }
</script>

<style lang="scss">
    .text-editor-container {
        height: 100%;
        position: relative;
        overflow: hidden;

        .text-editor {
            width: 100%;
            height: 100%;
            position: absolute;

            .CodeMirror {
                width: 100%;
                height: 100%;
            }
        }

        .saving {
            width: 80px;
            height: 30px;
            display: flex;
            justify-content: center;
            align-items: center;

            position: absolute;
            left: 0;
            right: 0;
            top: -30px;
            margin-left: auto;
            margin-right: auto;

            background: rgba(32, 73, 105, 0.7);
            border-radius: 0 0 5px 5px;
            color: white;
            transition: top 300ms;

            &.show {
                top: 0;
            }
        }
    }

</style>