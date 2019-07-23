<template>
    <div class="file" @dblclick="open"
         @contextmenu.prevent="contextmenu" @click="cancelUpload">
        <div class="file-icon" :class="{uploading:isUploading||isWaiting}">
            <img :src="file.thumbnail" v-if="image"/>
            <svg class="icon file-icon" aria-hidden="true" v-else>
                <use :xlink:href="'#'+icon"></use>
            </svg>
            <div class="state-icon-container" v-if="isNormal===false">
                <div v-if="isUploading">
                    <svg class="icon state-icon" aria-hidden="true">
                        <use xlink:href="#py_shangchuan"></use>
                    </svg>
                    <div>上传中</div>
                </div>
                <div v-else-if="isWaiting">
                    <svg class="icon state-icon" aria-hidden="true">
                        <use xlink:href="#py_yuyue-lishi-shijian"></use>
                    </svg>
                    <div>等待上传</div>
                </div>
            </div>
        </div>
        <div class="file-name">{{file.name}}</div>
        <div class="file-name-full">{{file.name}}</div>
    </div>
</template>

<script>
  import { File, FileState, FileType } from '../js/file'

  export default {
    props: { id: String, file: File },
    data() {
      return {
        image: null,
      }
    },
    computed: {
      icon() {
        switch(this.file.type) {
          case FileType.Folder:
            return Icons['folder']
          case FileType.Audio:
            return Icons['audio']
          case FileType.Video:
            return Icons['video']
          case FileType.Image:
            return Icons['image']
          case FileType.Text:
            return Icons['text']
          case FileType.Zip:
            return Icons['zip']
          case FileType.PDF:
            return Icons['pdf']
          case FileType.Word:
            return Icons['word']
          case FileType.Excel:
            return Icons['excel']
          case FileType.PPT:
            return Icons['ppt']
          case FileType.Code:
            return Icons['code']
          default:
            return Icons['default']
        }
      },
      isNormal() {
        return this.file.state === FileState.Normal
      },
      isUploading() {
        return this.file.state === FileState.Uploading
      },
      isWaiting() {
        return this.file.state === FileState.Waiting
      },
    },
    methods: {
      open() {
        if(this.file.state === FileState.Normal)
          this.$emit('dblclick', this.file)
      },
      contextmenu(e) {
        // 添加额外的右键菜单
        if(this.isWaiting || this.isUploading)
          this.$store.commit('appendMenuItem', {
            name: '取消上传', click: this.cancelUpload,
          })
        this.$store.commit('contextmenu', { e, id: this.id, file: this.file })
      },
      cancelUpload() {
        if(this.isNormal || this.isUploading)
          return
        if(confirm(`取消上传 ${this.file.name} ?`)) {
          const user = this.$store.state.windows[this.id].user
          this.$store.commit('cancelUploadByFile', { user, file: this.file })
        }
      },
    },
    mounted() {
      this.image = null
      if(this.file.type === FileType.Image) {
        const img = new Image()
        img.src = this.file.thumbnail
        img.addEventListener('load', () => {this.image = this.file.thumbnail})
      }
    },
  }
</script>

<style scoped lang="scss">
    .file {
        width: 100px;
        padding: 8px 0 0 2px;
        position: relative;

        &:hover {
            background: #E9EEF3;

            .file-name-full {
                position: absolute;
                display: block;
            }

            .file-name {
                display: none;
            }
        }


        div.file-icon {
            width: 100px;
            height: 60px;
            text-align: center;
            position: relative;

            /*图片文件的预览图片*/
            img {
                max-width: 80px;
                height: 60px;
            }

            /*文件svg图标*/
            svg.file-icon {
                width: 100px;
                height: 60px;
                text-align: center;
            }

            /*文件状态图标*/
            .state-icon-container {
                flex-direction: column;
                position: absolute;
                left: 0;
                top: 0;
                width: 100px;
                height: 60px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 12px;

                svg.state-icon {
                    width: 50px;
                    height: 30px;
                }
            }

            &.uploading .state-icon-container {
                background: rgba(211, 220, 230, 0.5);
            }

        }

        .file-name {
            width: 100px;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }

        .file-name, .file-name-full {
            font-size: 14px;
            text-align: center;
        }

        .file-name-full {
            width: 100px;
            display: none;
            white-space: pre-wrap;
            word-break: break-all;
            background: #E9EEF3;
            left: 0;
            padding-left: 2px;
            z-index: 1;
        }
    }
</style>