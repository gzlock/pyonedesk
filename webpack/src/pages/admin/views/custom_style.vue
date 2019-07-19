<template>
    <div>
        <div v-if="loading">
            读取中
        </div>
        <el-form v-else label-position="left" label-width="100px">
            <el-form-item>
                <a href="https://github.com/gzlock/pyonedesk/stylize.md" target="_blank">
                    <el-button type="primary">教程(连接到Github)</el-button>
                </a>
            </el-form-item>
            <el-form-item>
                <div slot="label">图标JS网址<br>
                    <el-button type="text" @click="reset('src')">单项还原</el-button>
                </div>
                <el-input v-model="form.icon.src">
                    <div slot="prepend">https:</div>
                </el-input>
            </el-form-item>
            <el-form-item>
                <div slot="label">文件图标ID<br>
                    <el-button type="text" @click="reset('icons')">单项还原</el-button>
                </div>
                <el-table :data="icons" border size="small">
                    <el-table-column prop="name" label="文件图标" width="140"/>
                    <el-table-column prop="value" label="ID">
                        <template slot-scope="scope">
                            <el-input size="small" v-model="form.icon.icons[scope.row.key]"></el-input>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
            <el-form-item>
                <div slot="label">CSS样式<br>
                    <el-button type="text" @click="reset('css')">单项还原</el-button>
                </div>
                <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="form.css"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit">保存</el-button>
                <el-button type="text" @click="reset('all')">全部还原</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
  import { API } from '../preset'

  export default {
    name: 'custom_style',
    data() {
      return {
        loading: true,
        ui: {
          default: '默认',
          user: '桌面的账号',
          folder: '文件夹',
          video: '视频文件',
          audio: '音频文件',
          image: '图片文件',
          text: '纯文本文件',
          code: '代码文件',
          zip: '压缩文件',
          pdf: 'PDF文件',
          word: 'Office Word',
          excel: 'Office Excel',
          ppt: 'Office PowerPoint',
        },
        default: {},//默认值
        form: {},//表单
      }
    },
    computed: {
      icons() {
        return Object.keys(this.form.icon.icons).map(key => {
          return { name: this.ui[key], key }
        })
      },
    },
    watch: {
      'form.icon.src': 'url',
    },
    methods: {
      url(url) {
        const replaces = ['http:', 'https:']
        replaces.forEach(re => {
          if(url.indexOf(re) > -1)
            url = url.replace(re, '')
        })
        this.form.icon.src = url
      },
      reset(type) {
        if(['src', 'icons', 'css', 'all'].indexOf(type) === -1)
          return
        let name
        switch(type) {
          case 'src':
            name = '图标JS网址'
            break
          case 'icons':
            name = '所有图标ID'
            break
          case 'css':
            name = 'CSS样式'
            break
          default:
            name = '全部自定义设置'
        }
        this.$confirm(`确认将 ${name} 还原为默认值?`).then(() => {

          switch(type) {
            case 'src':
              this.form.icon.src = this.default.icon.src
              break
            case 'icons':
              this.form.icon.icons = JSON.parse(JSON.stringify(this.default.icon.icons))
              break
            case 'css':
              this.form.css = this.default.css
              break
            default:
              this.form = JSON.parse(JSON.stringify(this.default))
          }

        }).catch(() => {})
      },
      async submit() {
        await this.$store.dispatch('api', { method: 'post', url: API.stylizes, data: this.form })
        this.$message.success('成功保存')
      },
    },
    async mounted() {
      const { data } = await this.$http.get(API.stylizes)
      this.form = data.custom
      this.default = data.default
      this.loading = false
    },
  }
</script>

<style scoped>

</style>