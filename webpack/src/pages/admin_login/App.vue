<template>
    <div>
        <el-dialog title="登录PyOneDrive管理后台" visible :show-close="false" :close-on-click-modal="false"
                   :close-on-press-escape="false">
            <el-form>
                <el-form-item label="密码">
                    <el-input v-model="password"/>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="login">登 录</el-button>
        </span>
        </el-dialog>
    </div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return { password: '' }
    },
    methods: {
      login() {
        if(!this.password)
          return this.$message.error('请填写密码')
        this.$http.post('/admin/login', { password: this.password }).then(res => {
          if(res.data.code === 1)
            window.location = '/admin'
          else
            this.$message.error('密码错误')
        })
      },
    },
  }
</script>

<style>
    body {
        background: #99a9bf;
    }

    .el-dialog {
        width: 500px !important;
    }
</style>