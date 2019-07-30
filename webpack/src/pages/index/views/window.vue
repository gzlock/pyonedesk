<template>
    <div class="window" :class="{active:$store.state.activeID === window.id,dragging,loading}" @focus="focus"
         :style="{'z-index':window.z}"
         :tabindex="window.z" @blur="blur">
        <div class="window--head">
            <div class="name"> {{current.name}}</div>
            <div class="controller" style="margin-right: 10px">
                <svg class="icon" aria-hidden="true" @click="load(true)" :class="{disabled:loading}">
                    <use xlink:href="#py_shuaxin"></use>
                </svg>
                <svg class="icon" aria-hidden="true" @click="go()" :class="{disabled:loading || historyIndex <= 0}">
                    <use xlink:href="#py_houtui"></use>
                </svg>
                <svg class="icon" aria-hidden="true" @click="go(1)"
                     :class="{disabled:loading || (historyIndex >= history.length-1)}">
                    <use xlink:href="#py_qianjin"></use>
                </svg>
            </div>
            <div class="controller">
                <svg class="icon" aria-hidden="true" @click="close">
                    <use xlink:href="#py_guanbi"></use>
                </svg>
            </div>
        </div>
        <div class="window--path">
            <el-breadcrumb separator="/" class="path">
                <el-breadcrumb-item></el-breadcrumb-item>
                <el-breadcrumb-item v-for="(file,i) in path" :key="i">
                    <a @click="go(-(path.length - i - 1))">{{file}}</a>
                </el-breadcrumb-item>
            </el-breadcrumb>

            <window-folder-tool v-show="loading === false && showFolder"
                                :window="window" :file="current" @upload="upload"/>

        </div>
        <div class="window--body" v-show="!dragging" :class="{loading:loading}">
            <window-loading v-if="loading"/>
            <window-error v-if="error" :error="error"/>
            <template v-show="!loading">
                <template v-if="showFolder">
                    <window-folder ref="content" :window="window" :file="current" @open="open"
                                   :loading.sync="loading" @loadError="loadError"/>
                </template>
                <template v-else-if="showEditor">
                    <window-editor ref="content" :window="window" :file="current" :loading.sync="loading"
                                   @loadError="loadError"/>
                </template>
                <template v-else-if="showViewer">
                    <window-viewer ref="content" :window="window" :file="current" :loading.sync="loading"
                                   @loadError="loadError"/>
                </template>
                <template v-else-if="showPlayer">
                    <window-player ref="content" :window="window" :file="current" :loading.sync="loading"
                                   @loadError="loadError"/>
                </template>
                <template v-else>
                    <window-binary-file ref="content" :window="window" :file="current" :loading.sync="loading"
                                        @loadError="loadError"/>
                </template>
            </template>
        </div>
    </div>
</template>

<script>
  import { FileType } from '../js/file'
  import { Window } from '../js/window'
  import WindowEditor from './window-editor'
  import WindowViewer from './window-viewer'
  import WindowPlayer from './window-player'
  import WindowFolder from './window-folder'
  import WindowLoading from './window-loading'
  import WindowError from './window-error'
  import WindowBinaryFile from './window-binary-file'
  import WindowFolderTool from './window-folder-tool'

  export default {
    components: {
      WindowFolderTool,
      WindowBinaryFile,
      WindowError,
      WindowLoading,
      WindowFolder,
      WindowPlayer,
      WindowViewer,
      WindowEditor,
    },
    props: { window: Window },
    data() {
      return {
        loading: true,
        dragging: false,
        zIndex: 0,
        active: true,
        history: [],
        historyIndex: 0,
        error: null,
      }
    },
    methods: {
      upload(type) {
        if(this.loading === false && this.$refs['content'].click_upload)
          this.$refs['content'].click_upload(type)
      },
      close() {
        this.$store.commit('closeWindow', this.window.id)
      },
      focus() {
        if(this.$store.state.activeID !== this.window.id)
          this.$store.commit('windowSetTop', this.window.id)
      },
      blur() {
        // console.log('blur', this.id)
      },
      loadError(error) {
        this.error = error
        this.loading = false
      },
      async load(force = false) {
        this.loading = true
        this.error = null
        this.$nextTick(() => {
          this.$refs['content'].load(force)
        })
      },
      open(file) {
        console.log('window.vue open', this.loading, file)
        if(this.loading)
          return

        this.history.splice(this.historyIndex + 1)
        this.append(file)
        this.historyIndex++
        this.load()
      },
      go(count = -1) {
        if(this.loading)
          return
        const test = this.historyIndex + count
        if(test >= 0 && test < this.history.length)
          this.historyIndex += count
      },
      append(file) {
        this.history.push(file)
      },
    },
    computed: {
      current() {
        return this.history[this.historyIndex]
      },
      showFolder() {
        return this.current.type === FileType.Folder
      },
      showPlayer() {
        return [FileType.Video, FileType.Audio].indexOf(this.current.type) !== -1
      },
      showEditor() {
        return [FileType.Code, FileType.Text].indexOf(this.current.type) !== -1
      },
      showViewer() {
        return [FileType.Image].indexOf(this.current.type) !== -1
      },
      path() {
        return this.history.slice(0, this.historyIndex + 1).map((file, i) => {
          if(i === 0)
            return this.window.user.name
          return file.name
        })
      },
    },
    async beforeMount() {
      this.append(this.window.file)
      await this.load()
    },
    watch: {},
    mounted() {
      //处理 拖动 和 缩放
      const $e = $(this.$el), $header = $e.find('.window--head')
      $e.mousedown(() => {
        this.focus()
      }).draggable({
        handle: $header,
        cancel: '.controller',
        start: () => {
          this.focus()
          this.dragging = true
        }, stop: () => {
          this.dragging = false
        },
      }).resizable({
        minHeight: 200,
        minWidth: 400,
        start: () => {
          this.dragging = true
        },
        stop: () => {
          this.dragging = false
        },
      })
    },
  }
</script>

<style lang="scss">
    .path > .el-breadcrumb__item > .el-breadcrumb__separator {
        margin: 0 3px !important;
    }
</style>
<style scoped lang="scss">
    @import '../../../assets/global.scss';

    .window {
        outline: none;
        position: absolute;
        background: rgba(255, 255, 255, 0.8);
        padding: 4px;
        display: flex;
        flex-direction: column;
        width: 400px;
        height: 200px;
        min-width: 400px;
        min-height: 200px;

        &.active {
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
        }

        &.loading {
            .window--body {
                overflow: hidden;
            }
        }

        .window--head {
            /*border-radius: 4px 4px 0 0;*/
            user-select: none;
            background: white;
            display: flex;
            height: 30px;

            .name {
                font-size: 16px;
                line-height: 30px;
                padding-left: 10px;
                box-sizing: content-box;
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .controller {
                svg.icon {
                    width: 30px;
                    height: 30px;
                    padding: 8px;
                    box-sizing: border-box;

                    &:hover {
                        background: #E9EEF3;
                    }

                    &.disabled {
                        fill: #999;
                        background: transparent !important;
                    }
                }
            }
        }

        .window--path {
            height: 26px;
            flex-shrink: 0;
            font-size: 12px;
            color: #ccc;
            border-top: 1px solid #ccc;
            border-bottom: 1px solid #eee;
            background: white;
            display: flex;
            align-items: center;
            padding-left: 10px;

            .path {
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
        }


        .window--body {
            flex-grow: 1;
            overflow: auto;
            background: white;
            position: relative;
        }
    }

</style>