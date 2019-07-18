<template>
    <div class="container" v-loading="loading">
        <el-form label-width="80px" :model="form" :rules="rules" ref="clientForm"
                 :label-position="$store.state.labelPosition">
            <el-form-item label="别名" prop="name">
                <el-input v-model="form.name"/>
            </el-form-item>
            <el-form-item label="应用名称">
                {{appName}}
            </el-form-item>
            <el-form-item>
                没有【应用ID】和【应用机密钥匙】？立即
                <create-app-button :account="form"/>
                <br>
                创建途中一定要记录下应用ID和应用机密钥匙，并填入到输入框。
            </el-form-item>
            <el-form-item label="应用 ID" prop="client_id">
                <el-input v-model="form.client_id" ref="client_id">
                    <el-button slot="prepend" @click="paste('client_id')">粘贴</el-button>
                </el-input>
            </el-form-item>
            <el-form-item label="应用机密" prop="client_secret">
                <el-input v-model="form.client_secret" ref="client_secret">
                    <el-button slot="prepend" @click="paste('client_secret')">粘贴</el-button>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit" :disabled="disabled">下一步</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
  import { API } from '../preset'
  import CreateAppButton from './create-app-button'

  export default {
    components: { CreateAppButton },
    data() {
      return {
        loading: true,
        form: { id: '', name: '', client_id: '', client_secret: '', code: '' },
        rules: {
          name: [
            { required: true, message: '请输入账号别名', trigger: 'blur' },
            {
              trigger: 'blur', validator: (rule, value, callback) => {
                value = value.trim()
                console.log('account', this.accounts)
                const keys = Object.keys(this.accounts)
                console.log('keys', keys)
                for(let i = 0; i < keys.length; i++) {
                  const account = this.accounts[keys[i]]
                  if(account.name === value)
                    return callback(new Error('已经有相同别名的账号了'))
                }
                callback()
              },
            },
          ],
          client_id: [
            { required: true, message: '请输入应用ID', trigger: 'blur' },
          ],
          client_secret: [
            { required: true, message: '请输入应用机密钥匙', trigger: 'blur' },
          ],
        },
      }
    },
    computed: {
      accounts() {
        return this.$store.state.accounts
      },
      appName() {
        return 'PyOneDrive-' + this.form.name
      },
      disabled() {
        return this.form.name.length === 0 || this.form.client_id.length === 0 || this.form.client_secret.length ===
          0 || this.loading
      },
    },
    methods: {
      async paste(refName) {
        this.form[refName] = await navigator.clipboard.readText()
      },
      async submit() {
        this.loading = true
        this.$refs['clientForm'].validate(async valid => {
          if(!valid)
            return
          const { data } = await this.$store.dispatch('api', {
            url: API.addAccount,
            method: 'post',
            data: this.form,
          })
          this.$store.state.accounts[data.id] = data
          this.loading = false
          this.$message({
            message: '成功添加账号，但还有最后一步操作',
            type: 'success',
          })
          this.$router.replace({ name: 'edit', params: { id: data.id } })
        })
      },
    },
    async mounted() {
      this.loading = true
      const { data } = await this.$store.dispatch('api', { url: API.createAccountID })
      this.form.id = data.id
      this.loading = false
    },
  }
</script>

<style lang="scss" scoped>
    .container {
        .el-form {
            margin: 20px 0 0 0;
        }
    }
</style>