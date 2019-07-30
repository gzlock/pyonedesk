<template>
    <div class="file" @dblclick="open"
         @contextmenu.prevent="contextmenu" @click="click">
        <div class="file-icon" :class="{uploading:isUploading||isWaiting}">
            <template v-if="image">
                <img :src="file.thumbnail" alt="图片"/>
                <svg class="icon video-play-icon" aria-hidden="true" v-if="isVideo">
                    <use xlink:href="#py_play"></use>
                </svg>
            </template>
            <file-icon v-else :file="file"/>
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
        <div class="file-name">
            <div class="file-name__ellipsis">{{file.name}}</div>
            <div class="file-name__full">{{file.name}}</div>
        </div>
    </div>
</template>

<script>
  import { File, FileState, FileType } from '../js/file'
  import FileIcon from './file-icon'

  export default {
    components: { FileIcon },
    props: { id: String, parent: File, file: File },
    data() {
      return {
        image: null,
      }
    },
    computed: {
      isNormal() {
        return this.file.state === FileState.Normal
      },
      isUploading() {
        return this.file.state === FileState.Uploading
      },
      isWaiting() {
        return this.file.state === FileState.Waiting
      },
      isUploadFail() {
        return this.file.state === FileState.UploadFail
      },
      isVideo() {
        return this.file.type === FileType.Video
      },
    },
    methods: {
      open() {
        console.log('open', this.file)
        if(this.file.state === FileState.Normal)
          this.$emit('dblclick', this.file)
      },
      contextmenu(e) {
        // 添加额外的右键菜单
        if(this.isWaiting || this.isUploading)
          this.$store.commit('appendMenuItem', {
            name: '取消上传', click: this.click,
          })
        this.$store.commit('contextmenu', { e, id: this.id, file: this.file })
      },
      click() {
        if(this.isNormal || this.isUploading)
          return
        console.log('file click', { isWaiting: this.isWaiting, isUploadFail: this.isUploadFail })
        if(this.isWaiting) {
          this.$confirm(`取消上传 ${this.file.name} ？`).then(() => {
            this.$store.commit('cancelUploadFile', this.file)
          }).catch(() => {})
        } else if(this.isUploadFail) {
          const reason = this.file.reason || ''
          this.$confirm(`上传失败原因：${reason}`, `再次尝试上传 ${this.file.name} ？`).then(() => {
            const data = this.$store.getters.getUploadingDataByFile(this.file)
            if(data) {
              this.$store.commit('uploadQueuePush', data)
            }
          }).catch(() => {})
        }
      },
      loadThumbnail() {
        this.image = null
        if(this.file.state === FileState.Normal &&
          [FileType.Image, FileType.Video].indexOf(this.file.type) > -1 &&
          this.file.thumbnail) {
          const img = new Image()
          img.src = this.file.thumbnail
          img.addEventListener('load', () => {this.image = this.file.thumbnail})
        }
      },
    },
    watch: {
      file() {
        this.loadThumbnail()
      },
    },
    mounted() {
      this.loadThumbnail()
    },
  }
</script>

<style scoped lang="scss">
    @keyframes play-icon-animation {
        0% {
            fill-opacity: 1;
        }
        100% {
            fill-opacity: 0.5;
        }
    }

    .file {
        width: 100px;
        padding: 8px 0 0 0;
        position: relative;
        border-radius: 8px;

        &:hover {
            background: #E9EEF3;


            .file-name {
                .file-name__full {
                    position: absolute;
                    display: block;
                    direction: ltr;
                }
            }

            .video-play-icon {
                animation: play-icon-animation .5s alternate infinite ease-in-out;
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

            .video-play-icon {
                position: absolute;
                left: 0;
                right: 0;
                top: 0;
                margin: 0 auto;
                width: 80px;
                height: 60px;
                fill-opacity: 1;
                fill: white;
                filter: drop-shadow(0px 0px 2px rgba(0, 0, 0, .7));
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
            position: relative;

            .file-name__ellipsis, .file-name__full {
                font-size: 14px;
                text-align: center;
            }

            .file-name__ellipsis {
                width: 100px;
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            .file-name__full {
                width: 100px;
                display: none;
                white-space: pre-wrap;
                word-break: break-word;
                background: #E9EEF3;
                left: 0;
                top: 0;
                z-index: 1;
                border-radius: 0 0 8px 8px;
            }
        }
    }
</style>