<template>
    <a :href="href" target="_blank">
        <el-button>创建微软应用</el-button>
    </a>
</template>

<script>
  import { API } from '../preset'

  export default {
    props: ['account'],
    computed: {
      href() {
        return `${API.goCreateAppUrl}/${this.account.id}/${this.account.name}`
      },
    },
  }
</script>

<style scoped>

</style>