<template>
    <div>
        <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
    </div>
</template>

<script>
  import { Index } from './preset'

  export default {
    data() {
      return {
        defaultProps: {
          children: 'children',
          label: 'label',
        },
        data: [],
      }
    },
    methods: {
      handleNodeClick(data) {
        console.log(data)
      },
    },
    async beforeMount() {
      const res = await this.$store.dispatch('api', { url: Index.accounts })
      this.data.length = 0
      for(let key in res.data) {
        const account = res.data[key]
        this.data.push({ label: '账号：' + account.name, children: [] })
      }
    },
  }
</script>

<style scoped>

</style>