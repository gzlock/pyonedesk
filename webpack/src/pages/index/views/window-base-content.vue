<template>
    <div>
    </div>
</template>

<script>
  export default {
    name: 'window-base-content',
    data() {return { loading: false }},
    methods: {
      async load(force = false) {
        // console.log('base content load()')
        if(this.loading)
          return
        this.loading = true
        if(this.loadContent)
          await this.loadContent(force)
        this.loading = false
        this.$emit('loadFinish')
      },
    },
    mounted() {
      this.load()
    },
  }
</script>

<style scoped>

</style>