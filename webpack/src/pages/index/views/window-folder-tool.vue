<template>
    <div class="tool-container">
        <div>
            <el-popover
                    placement="bottom"
                    width="160"
                    v-model="search.visible">
                <p>
                    <el-input placeholder="输入要搜索的内容" v-model="search.word" @keypress.native.enter="searchFile"/>
                </p>
                <div style="text-align: right; margin: 0">
                    <!--                <el-button size="mini" type="text" @click="searchVisible = false">取消</el-button>-->
                    <el-button type="primary" size="mini" @click="searchFile">搜索</el-button>
                </div>
                <el-button slot="reference" type="text" size="mini">搜索</el-button>
            </el-popover>
        </div>
        <el-dropdown @command="sortFile" size="mini" trigger="click">
                  <span class="el-dropdown-link">
                    排序<i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="(item,i) in sortItems" :key="i"
                                  :class="{current:item.type === sort.type}" :command="item.command"
                                  :icon="sortIcon(item.type)">
                    {{item.name}}
                </el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <el-dropdown @command="create" size="mini" trigger="click">
                  <span class="el-dropdown-link">
                    创建<i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="folder">文件夹</el-dropdown-item>
                <el-dropdown-item divided></el-dropdown-item>
                <el-dropdown-item command="text">文本文件</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <el-dropdown type="text" @click="upload('file')" @command="upload" size="mini" trigger="hover"
                     split-button>
            上传
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="file">文件</el-dropdown-item>
                <el-dropdown-item command="folder">文件夹</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<script>
  import { defaultSort, File, FileSortType, FileType } from '../js/file'
  import { Window, WindowEvent } from '../js/window'

  export default {
    name: 'window-folder-tool',
    props: { window: Window, file: File },
    data() {
      return {
        sort: JSON.parse(JSON.stringify(defaultSort)),
        search: { visible: false, word: '' },
      }
    },
    watch: {
      file() {
      },
    },
    methods: {
      upload(type) {
        this.$emit('upload', type)
      },
      create(command) {
        if(command === 'folder') {
          this.$prompt('输入文件夹名称', '创建文件夹').then(({ value }) => {
            this.$refs['content'].create(FileType.Folder, value)
          }).catch(() => {})
        } else if(command === 'text') {
          this.$prompt('输入文本文件名称', '创建文本文件').then(({ value }) => {
            this.$refs['content'].create(FileType.Text, value)
          }).catch(() => {})
        }
      },
      sortFile(type) {
        switch(type) {
          case 'name':
            if(this.sort.type === FileSortType.Name)
              this.sort.isUp = !this.sort.isUp
            else
              this.sort.isUp = false
            this.sort.type = FileSortType.Name
            break
          case 'size':
            if(this.sort.type === FileSortType.Size)
              this.sort.isUp = !this.sort.isUp
            else
              this.sort.isUp = false
            this.sort.type = FileSortType.Size
            break
          case 'cTime':
            if(this.sort.type === FileSortType.CreatedTime)
              this.sort.isUp = !this.sort.isUp
            else
              this.sort.isUp = false
            this.sort.type = FileSortType.CreatedTime
            break
          case 'mTime':
            if(this.sort.type === FileSortType.ModifiedTime)
              this.sort.isUp = !this.sort.isUp
            else
              this.sort.isUp = false
            this.sort.type = FileSortType.ModifiedTime
            break
          default:
            break
        }
        this.window.trigger(WindowEvent.SortFile, this.sort)
      },
      searchFile() {
        this.window.trigger(WindowEvent.SearchFile, this.search.word)
      },
      sortIcon(sort) {
        if(sort !== this.sort.type)
          return ''
        return this.sort.isUp ? 'el-icon-top' : 'el-icon-bottom'
      },
    },
    computed: {
      sortItems() {
        return [
          { name: '名称', command: 'name', type: FileSortType.Name },
          // { name: '大小', command: 'size', type: FileSortType.Size },
          // { name: '创建时间', command: 'cTime', type: FileSortType.CreatedTime },
          // { name: '修改时间', command: 'mTIme', type: FileSortType.ModifiedTime },
        ]
      },
    },
  }
</script>

<style lang="scss">
    .tool-container {
        > .el-dropdown > .el-button-group .el-button--text {
            color: #606266 !important;
        }
    }

    .el-dropdown-menu {
        .current {
            color: red;
        }
    }
</style>
<style scoped lang="scss">
    .tool-container {
        display: flex;
        height: 100%;

        .el-dropdown, .el-dropdown .el-button-group .el-button--text {
            font-size: 12px !important;
            color: #606266 !important;
        }


        div {
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            padding: 0 5px;
            height: 100%;

            * {
                color: #606266 !important;
            }


            & + div {
                margin-left: 10px;
            }

            &:hover {
                background: #D3DCE6;
            }
        }

        svg.icon {
            width: 14px;
            height: 14px;
            margin-right: 5px;
        }

        .el-dropdown {
            .el-dropdown-menu__item .current {
                color: red;
            }
        }
    }
</style>