<template>
    <div>
        <template v-if="state === 1">
            <i class="el-icon-loading"></i>正在等待结果
        </template>
        <template v-else-if="state === 2">
            <i class="el-icon-success" style="color: green;"></i>接收 Code 成功！
        </template>
        <template v-else>
            <div v-if="state === 3">
                <i class="el-icon-error" style="color: red;"></i>接收到的 Code 无效，请重试！
            </div>
            <div v-else-if="state === 4">
                <i class="el-icon-error" style="color: red;"></i>接收 Code 超时，请重试！
            </div>
            <!--<a target="_blank" :href="href">
                <el-button @click="addLocalStorageListener" type="primary">前往微软网站获取Code</el-button>
            </a>-->
            <el-button @click="addLocalStorageListener" type="primary">前往微软网站获取Code</el-button>
        </template>
    </div>
</template>

<script>
  import { API } from '../preset'

  export default {
    props: ['account'],
    data() {
      /***
       * state 状态：
       * 0 未点击按钮状态
       * 1 点击后，等待反馈
       * 2 成功
       * 3 code 无效
       * 4 超时
       */
      return { state: 0 }
    },
    methods: {
      addLocalStorageListener() {
        window.open(this.href)
        this.state = 1
        window.localStorage.removeItem(this.account.id)
        let timeout
        const listener = e => {
          console.log('localstorage', e)
          if(e === 'timeout')
            this.state = 4
          else if(e && e.key === this.account.id && Number(e.newValue) === 1) {
            this.state = 2
            this.$emit('success')
          } else
            this.state = 3
          window.removeEventListener('storage', listener)
          clearTimeout(timeout)
        }
        window.addEventListener('storage', listener)
        timeout = setTimeout(() => {listener('timeout')}, 10000)
      },
    },
    computed: {
      href() {
        return API.goGetCode + '/' + this.account.id
      },
    },
  }
</script>

<style scoped>

</style>