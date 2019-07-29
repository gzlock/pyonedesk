<template>
    <el-button @click="open" :disabled="account.name.length === 0">创建微软应用</el-button>
</template>

<script>
  import { API } from '../preset'

  export default {
    props: ['account'],
    computed: {
      href() {
        return `${API.goCreateAppUrl}/${this.account.id}/${this.account.name}?origin=` + window.location.origin
      },
    },
    methods: {
      open() {
        window.open(this.href)
      },
    },
  }
</script>

<style scoped>

</style>