<template>
    <div v-loading="loading">
        <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane label="账号容量" name="quota" :disabled="!account.has_token">
                <el-form label-width="120px">
                    <el-form-item label="别名">{{account.name}}</el-form-item>
                    <el-form-item label="账号状态">{{account.quota.state}}</el-form-item>
                    <el-form-item label="总容量">{{bytesToSize(account.quota.total)}}</el-form-item>
                    <el-form-item label="可用容量">{{bytesToSize(account.quota.remaining)}}</el-form-item>
                    <el-form-item label="已经使用容量">{{bytesToSize(account.quota.used)}}</el-form-item>
                    <el-form-item label="回收站占用容量">{{bytesToSize(account.quota.deleted)}}</el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="账号管理" name="info">
                <el-form label-width="100px" :label-position="$store.state.labelPosition">
                    <el-form-item label="默认账号">
                        <el-switch
                                v-model="account.default"
                                active-color="#13ce66"
                                inactive-color="#ff4949">
                        </el-switch>
                    </el-form-item>
                    <el-form-item>
                    </el-form-item>
                    <el-form-item label="账号别名">
                        <el-input v-model="account.name"/>
                    </el-form-item>
                    <el-form-item label="应用名称">
                        PyOneDrive-{{account.name}}

                        <a :href="'https://apps.dev.microsoft.com/#/application/'+account.client_id" target="_blank">
                            <el-button type="text">前往微软网站管理应用</el-button>
                        </a>
                    </el-form-item>
                    <el-form-item label="应用ID">
                        {{account.client_id}}
                    </el-form-item>
                    <el-form-item label="应用机密钥匙">
                        {{account.client_secret}}
                    </el-form-item>
                    <el-form-item label="refresh_token" v-if="account.has_token">
                        <el-input :value="account.refresh_token" disabled/>
                    </el-form-item>
                    <el-form-item>
                        <div slot="label" v-if="account.has_token">更换Code</div>
                        <div slot="label" class="red" v-else>最后一步<br>获取Code</div>
                        <el-input v-model="account.code"
                                  :placeholder="account.has_token ? '不更换Code请留空' :'填入Code'"></el-input>
                        <a target="_blank" :href="getCodeUrl">
                            <el-button type="text">前往微软网站获取Code</el-button>
                        </a>
                    </el-form-item>
                    <el-form-item label="操作">
                        <el-button type="primary" @click="save">保存设置</el-button>
                        <el-button type="danger" @click="deleteAccount">⚠️删除账号</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
  import { API } from '../preset'

  let watcher
  export default {
    data() {
      return {
        loading: true,
        activeName: '',
        account: { quota: {} },
        hideToken: true,
      }
    },
    computed: {
      id() {
        return this.$route.params.id
      },
      tokenString() {
        return JSON.stringify(this.account.token, null, 4)
      },
      getCodeUrl() {
        return API.goGetCode + '/' + this.account.id
      },
    },
    watch: {
      '$route.params.id'() {
        console.log('$route.params.id', '有变化')
        this.load()
      },
    },
    methods: {
      async load() {
        if(watcher)
          watcher()
        this.loading = true
        const { data } = await this.$store.dispatch('api', { url: API.account + '/' + this.id })
        this.account = data
        const accounts = this.$store.state.accounts
        accounts[this.account.id] = this.account
        this.$store.commit('setAccounts', accounts)
        this.loading = false
        this.activeName = this.account.has_token ? 'quota' : 'info'
      },
      bytesToSize(bytes) {
        if(bytes === 0) return '0 B'
        const k = 1024, // or 1024
          sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
          i = Math.floor(Math.log(bytes) / Math.log(k))

        return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i]
      },
      async deleteAccount() {
        try {
          await this.$confirm('确认删除账号：' + this.account.name + '?', '请确认', { type: 'warning' })
          const res = await this.$store.dispatch('api', { url: API.deleteAccount + '/' + this.id })
          if(!res)
            return
          this.$alert('成功删除账号：' + this.account.name)
          delete this.$store.state.accounts[this.id]
          this.$router.replace('/')
        } catch(e) {
          //
        }
      },
      get_code_finish() {
        console.log('code有效，重新读取')
        this.load()
      },
      async save() {
        this.loading = true
        const res = await this.$store.dispatch('api',
          { method: 'post', url: API.account + '/' + this.account.id, data: this.account })
        const id = this.account.default ? this.account.id : ''
        this.$store.commit('updateDefaultAccount', id)
        if(res !== null)
          this.$message.success('保存成功')
        this.loading = false
      },
    },
    async beforeMount() {
      await this.load()
    },
  }
</script>

<style scoped lang="scss">
    .red {
        color: red;

        .el-form-item__label {
            color: red;
        }
    }

    .token-textarea {
        font-size: 16px;
        width: 100%;
        height: 300px;
    }
</style>