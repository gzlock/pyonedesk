<template>
    <el-dialog visible title="从微软接收Code的结果">
        <div v-if="state === 1">
            Code验证可用并成功保存：{{code}}
            <br>
            小伙子你现在可以关闭这个页面了
            <div v-if="autoClose">
                <span style="color:red">{{countdown}} 秒</span> 后自动关闭该页面
            </div>
        </div>
        <div v-else>
            ⚠️Code {{code}} 无效
            <br>
            请再次从管理后台点击【获取Code】的按钮
        </div>
    </el-dialog>
</template>

<script>
  const countdown = 5
  export default {
    data() {
      // 关于 data 数据，请查看 server/admin.py get_code 函数
      return { ...window.data, countdown, autoClose: false } // eslint-disable-line
      /***
       * state 状态：
       * 0 code 无效
       * 1 成功
       */
    },
    methods: {
      close() {
        this.countdown--
        if(this.countdown <= 0)
          window.close()
        else
          setTimeout(this.close, 1000)
      },
    },
    mounted() {
      this.autoClose = window.opener !== null
      console.log('发送state', this.account.id, this.state)
      window.localStorage.setItem(this.account.id, this.state)
      if(this.state === 1 && this.autoClose) {
        // 有opener代表是用window.open打开的网页，可以用window.close关闭
        setTimeout(this.close, 1000)
      }
    },
  }
</script>

<style scoped>

</style>