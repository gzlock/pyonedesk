<template>
    <div class="file" @dblclick="$emit('dblclick',file)"
         @contextmenu.prevent="e=>$store.commit('showMenu',{e,id,file})">
        <div class="file-icon" v-if="image"><img :src="file.thumbnail"/></div>
        <svg class="icon file-icon" aria-hidden="true" v-else>
            <use :xlink:href="'#'+icon"></use>
        </svg>
        <div class="file-name">{{file.name}}</div>
    </div>
</template>

<script>
  import { File, FileType } from '../js/file'

  export default {
    props: { id: String, file: File },
    data() {return { image: null }},
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
    },
    mounted() {
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

        &:hover {
            background: #E9EEF3;
            border-radius: 5px;
        }

        svg.file-icon {
            width: 100px;
            height: 60px;
            text-align: center;
        }

        div.file-icon {
            width: 100px;
            height: 60px;
            text-align: center;

            img {
                height: 60px;
            }
        }

        .file-name {
            max-width: 100px;
            font-size: 14px;
            text-align: center;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
    }
</style>