<template>
    <svg class="icon file-icon" aria-hidden="true">
        <use :xlink:href="'#'+icon"></use>
    </svg>
</template>

<script>
  import { FileType } from '../js/file'

  export default {
    name: 'file-icon',
    props: ['file'],
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
  }
</script>

<style scoped>

</style>