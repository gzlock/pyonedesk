<template>
    <div>
    </div>
</template>

<script>
  export default {
    name: 'window-base-content',
    data() {
      return {
        loading: false,
      }
    },
    methods: {
      async load(force = false) {
        // console.log('base content load()')
        if(this.loading)
          return
        this.$emit('update:loading', true)
        this.loading = true
        if(this.loadContent)
          await this.loadContent(force)
        this.loading = false
        this.$emit('update:loading', false)
      },
    },
    mounted() {
      this.load()
    },
  }
</script>

<style scoped>

</style>