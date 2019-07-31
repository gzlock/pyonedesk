<template>
    <div class="file-container">
        <file-icon :type="info.type"/>
        <el-form label-width="80px">
            <el-form-item label="文件名">{{file.name}}</el-form-item>
            <el-form-item label="大小">{{bytesToSize(info.size)}}</el-form-item>
            <el-form-item label="创建时间">{{info.createdTime}}</el-form-item>
            <el-form-item label="修改时间">{{info.modifiedTime}}</el-form-item>
            <el-form-item>
                <a :href="info.url" target="_blank">
                    <el-button type="text">下载</el-button>
                </a>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
  import WindowBaseContent from './window-base-content'
  import { join } from 'path'
  import FileIcon from './file-icon'
  import { Window } from '../js/window'
  import { File, GetFileType } from '../js/file'
  import { get } from 'lodash'
  import { bytesToSize } from '../../../js/utils'

  export default {
    name: 'window-binary-file',
    components: { FileIcon },
    extends: WindowBaseContent,
    props: { window: Window, file: File },
    data() {
      return {
        info: {
          type: null,
          size: 0,
          createdTime: '',
          modifiedTime: '',
          url: '',
        },
      }
    },
    methods: {
      async loadContent(force = false) {
        const path = ':' + join(this.file.path, this.file.name)
        const { data } = await this.$store.dispatch('load', { user: this.window.user, path: path, force })
        console.log('文件', data)
        this.$emit('loadFinish')
        this.info.size = data.size
        this.info.url = data['@microsoft.graph.downloadUrl']
        this.info.createdTime = moment(new Date(data['createdDateTime'])).format('llll')
        this.info.modifiedTime = moment(new Date(data['lastModifiedDateTime'])).format('llll')

        this.info.type = GetFileType(data['name'], get(data, 'file.mimeType'))
      },
      bytesToSize: bytesToSize,
    },
  }
</script>

<style scoped lang="scss">
    .file-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .file-icon {
            width: 140px
        }

        .el-form {
            .el-form-item {
                margin-bottom: 0 !important;
            }
        }
    }
</style>