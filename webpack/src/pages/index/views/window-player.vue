<template>
    <div class="player">
    </div>
</template>

<script>
  import WindowBaeContent from './window-base-content'

  export default {
    extends: WindowBaeContent,
    name: 'window-player',
    props: ['user', 'file'],
    data() {
      return {}
    },
    methods: {
      async loadContent(force) {
        console.log('player mounted')
        const path = `:${this.file.path}`
        const { data } = await this.$store.dispatch('load', { user: this.user, path, force })
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