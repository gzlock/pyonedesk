<template>
    <div>
        <div v-if="loading">
            读取中
        </div>
        <el-form v-else>
            <el-form-item>
                <a href="https://github.com/gzlock/pyonedesk/stylize.md" target="_blank">
                    <el-button type="primary">教程(连接到Github)</el-button>
                </a>
            </el-form-item>
            <el-form-item label="图标JS网址">
                <el-input v-model="form.icon.src">
                    <div slot="prepend">https:</div>
                </el-input>
            </el-form-item>
            <el-form-item>
                <!--<div v-for="(icon,key) in form.icon.icons" :key="key" style="clear: both">
                    {{key}}
                    <el-input size="small" v-model="form.icon.icons[key]"/>
                </div>-->
                <el-tabs tab-position="left">
                    <el-tab-pane :label="ui[key]" v-for="(icon,key) in form.icon.icons" :key="key">
                        <el-input size="small" v-model="form.icon.icons[key]"/>
                    </el-tab-pane>
                </el-tabs>
            </el-form-item>
            <el-form-item label="CSS样式">
                <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="form.css"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit">提交</el-button>
                <el-button type="text" @click="reset">还原</el-button>
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
          word: 'Office Word',
          excel: 'Office Excel',
          ppt: 'Office PowerPoint',
        },
        default: {},//默认值
        form: {},//表单
      }
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
      reset() {
        this.$confirm('确认将全部设置还原为默认值?').then(() => {
          this.form = JSON.parse(JSON.stringify(this.default))
        }).catch(() => {})
      },
      submit() {
        console.log(this.form.icon.icons['default'])
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