<template>
    <div class="window" :class="{active:$store.state.activeID === id,dragging,loading}" @focus="focus"
         :style="{'z-index':z}"
         :tabindex="z" @blur="blur">
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

            <div class="controller" v-if="loading === false && showFolder">
                <el-dropdown @command="create" size="mini" trigger="click">
                  <span class="el-dropdown-link">
                    创建<i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="folder">文件夹</el-dropdown-item>
                        <el-dropdown-item divided></el-dropdown-item>
                        <el-dropdown-item command="text">文本文件</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <div @click="upload('file')">
                    <svg class="icon" aria-hidden="true" :class="{disabled:loading}">
                        <use xlink:href="#py_shangchuan1"></use>
                    </svg>
                    文件
                </div>
                <div @click="upload('folder')">
                    <svg class="icon" aria-hidden="true" :class="{disabled:loading}">
                        <use xlink:href="#py_shangchuan1"></use>
                    </svg>
                    文件夹
                </div>
            </div>
        </div>
        <div class="window--body" v-show="!dragging" :class="{loading:loading}">
            <window-loading v-if="loading"/>
            <window-error v-if="error" :error="error"/>
            <template v-show="!loading">
                <template v-if="showFolder">
                    <window-folder ref="content" :user="user" :id="id" :file="current" @open="open"
                                   @loadFinish="loadFinish" @loadError="loadError"/>
                </template>
                <template v-else-if="showEditor">
                    <window-editor ref="content" :user="user" :file="current" @loadFinish="loadFinish"
                                   @loadError="loadError"/>
                </template>
                <template v-else-if="showViewer">
                    <window-viewer ref="content" :user="user" :file="current" @loadFinish="loadFinish"
                                   @loadError="loadError"/>
                </template>
                <template v-else-if="showPlayer">
                    <window-player ref="content" :user="user" :file="current" @loadFinish="loadFinish"
                                   @loadError="loadError"/>
                </template>
            </template>
        </div>
    </div>
</template>

<script>
  import { File, FileType } from '../js/file'
  import { User } from '../js/user'
  import WindowEditor from './window-editor'
  import WindowViewer from './window-viewer'
  import WindowPlayer from './window-player'
  import WindowFolder from './window-folder'
  import WindowLoading from './window-loading'
  import WindowError from './window-error'

  export default {
    components: { WindowError, WindowLoading, WindowFolder, WindowPlayer, WindowViewer, WindowEditor },
    props: { id: String, user: User, file: File, z: Number },
    data() {
      return {
        loading: false,
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
        this.$store.commit('closeWindow', this.id)
      },
      focus() {
        if(this.$store.state.activeID !== this.id)
          this.$store.commit('windowSetTop', this.id)
      },
      blur() {
        // console.log('blur', this.id)
      },
      loadFinish() {
        this.loading = false
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
      create(command) {
        if(command === 'folder') {
          this.$prompt('输入文件夹名称', '创建文件夹').then(({ value }) => {
            this.$refs['content'].create(FileType.Folder, value)
          }).catch(() => {})
        } else if(command === 'text') {
          this.$prompt('输入文本文件名称', '创建文本文件').then(({ value }) => {
            this.$refs['content'].create(FileType.Text, value)
          }).catch(() => {})
        }
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
            return this.user.name
          return file.name
        })
      },
    },
    async beforeMount() {
      this.append(this.file)
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
        minHeight: 150,
        minWidth: 200,
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


<style scoped lang="scss">
    @import '@/assets/global.scss';

    .window {
        outline: none;
        position: absolute;
        background: rgba(255, 255, 255, 0.8);
        padding: 4px;
        display: flex;
        flex-direction: column;
        width: 400px;
        height: 200px;
        min-width: 200px;
        min-height: 150px;

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

            .controller {
                display: flex;
                color: black;
                height: 100%;

                div {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    cursor: pointer;
                    padding: 0 5px;
                    height: 100%;

                    & + div {
                        margin-left: 10px;
                    }

                    &:hover {
                        background: #D3DCE6;
                    }
                }

                svg.icon {
                    width: 14px;
                    height: 14px;
                    margin-right: 5px;
                }
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