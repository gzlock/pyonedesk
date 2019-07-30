<template>
    <div class="player">
    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'
  import { join } from 'path'
  import { Window } from '../js/window'
  import { File } from '../js/file'

  export default {
    extends: WindowBaeContent,
    name: 'window-player',
    props: { window: Window, file: File },
    data() {
      return {}
    },
    methods: {
      async loadContent(force) {
        console.log('player mounted')
        const path = ':' + join(this.file.path, this.file.name)
        const { data } = await this.$store.dispatch('load', { user: this.window.user, path, force })
        console.log('player', path, data)
        new DPlayer({
          container: this.$el,
          video: { url: data['@microsoft.graph.downloadUrl'] },
        })
      },
    },
    mounted() {
      this.load()
    },
  }
</script>

<style scoped lang="scss">
    .player {
        width: 100%;
        height: 100%;

        &.loading {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }
</style>