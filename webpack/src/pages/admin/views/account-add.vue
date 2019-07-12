<template>
    <div class="container">
        <el-steps :active="activeIndex" finish-status="success" align-center>
            <el-step title="OneDrive账号别名"></el-step>
            <el-step title="OneDrive应用信息"></el-step>
            <el-step title="获取Code"></el-step>
        </el-steps>
        <!--    填写别名    -->
        <div v-if="activeIndex===0">
            <el-form label-width="80px" :model="form" :rules="rules" ref="nameForm"
                     :label-position="$store.state.labelPosition">
                <el-form-item label="别名" prop="name">
                    <el-input v-model="form.name"/>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="checkName">下一步</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!--    填写应用ID和应用Secret    -->
        <div v-else-if="activeIndex === 1">
            <el-form label-width="80px" :model="form" :rules="rules" ref="clientForm"
                     :label-position="$store.state.labelPosition">
                <el-form-item label="应用名称">
                    {{appName}}
                </el-form-item>
                <el-form-item>
                    没有【应用ID】和【应用机密钥匙】？立即<br>
                    <create-app-button :account="form"/>
                    <br>
                    创建途中一定要记录下应用ID和应用机密钥匙，并填入到输入框。
                    <!--<el-button type="text" @click="showImage=true">查看示意图</el-button>-->
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
                    <el-button type="primary" @click="checkClientInfo">下一步</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!--    获取Code    -->
        <div v-else-if="activeIndex === 2">
            <div>最后一步，获取Code</div>
            <get-code-view :account="form" @success="finish"/>
        </div>
    </div>
</template>

<script>
  import GetCodeView from './get-code-view'
  import { API } from '../preset'
  import CreateAppButton from './create-app-button'

  export default {
    components: { CreateAppButton, GetCodeView },
    data() {
      return {
        activeIndex: 0,
        form: { id: '', name: '', client_id: '', client_secret: '', code: '' },
        showImage: false,
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
    },
    methods: {
      async paste(refName) {
        this.form[refName] = await navigator.clipboard.readText()
      },
      async checkName() {
        this.$refs['nameForm'].validate(async valid => {
          if(!valid)
            return
          this.activeIndex++
          const { data } = await this.$store.dispatch('api', { url: API.createAccountID })
          this.form.id = data.id
        })
      },
      async checkClientInfo() {
        this.$refs['clientForm'].validate(async valid => {
          if(!valid)
            return
          const { data } = await this.$store.dispatch('api', {
            url: API.addAccount,
            method: 'post',
            data: this.form,
          })
          this.$store.state.accounts[data.id] = data
          this.activeIndex++
        })
      },
      finish() {
        this.activeIndex = 3
      },
    },
    mounted() {
      console.log('add', this.accounts)
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