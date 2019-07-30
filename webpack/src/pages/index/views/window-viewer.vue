<template>
    <div class="image-viewer">
        <img :src="src" alt="图片" v-if="!loading">
    </div>

</template>

<script>
  import WindowBaeContent from './window-base-content'
  import { Window } from '../js/window'
  import { File } from '../js/file'

  export default {
    extends: WindowBaeContent,
    name: 'window-viewer',
    props: { window: Window, file: File },
    data() {
      return {
        src: '',
      }
    },
    methods: {
      async loadContent(force) {
        const path = ':' + this.file.path + '/' + this.file.name
        const { data: msData } = await this.$store.dispatch('load', { user: this.window.user, path, force })
        this.src = msData['@microsoft.graph.downloadUrl']

        const img = new Image()
        img.src = this.src
        await new Promise(resolve => {
          img.addEventListener('load', () => {
            resolve()
          })
          // 10秒超时
          setTimeout(() => {resolve()}, 10000)
        })
      },
    },
  }
</script>

<style scoped lang="scss">
    .image-viewer {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #666;
        min-height: 100%;

        img {
        }
    }
</style>