<template>
    <div class="contextmenu full" @click="hide" v-if="value" :style="{'z-index':$store.state.z}"
         @contextmenu.prevent="hide">
        <div :style="{left:offsetX,top:offsetY}" class="contextmenu-list">
            <div v-for="(item,i) in list" :key="i" @click="item.click">{{item.name}}</div>
        </div>
    </div>
</template>

<script>
  import { FileState, FileType } from '../js/file'
  import { WindowEvent } from '../js/window'
  import { join } from 'path'

  export default {
    name: 'contextmenu',
    props: ['value', 'x', 'y', 'id', 'file'],
    data() {return { list: [] }},
    methods: {
      hide() {
        this.$emit('input', false)
        this.$store.state.menuExtraItems.length = 0 // 清空额外项目
      },
    },
    computed: {
      offsetX() {
        return this.x + 2 + 'px'
      },
      offsetY() {
        return this.y + 2 + 'px'
      },
    },
    watch: {
      file() {
        const win = this.$store.state.windows[this.id], user = win.user
        this.list.length = 0
        if(this.file.state === FileState.Normal) {
          if([FileType.Folder, FileType.Text, FileType.Code, FileType.Image, FileType.Video, FileType.Audio].indexOf(
            this.file.type) > -1) {
            this.list.push({
              name: '新窗口打开',
              click: () => {this.$store.commit('createWindowFromMenu', { file: this.file })},
            })
          }
          if(this.file.type !== FileType.Folder) {
            this.list.push({
              name: '下载文件',
              click: () => {
                window.open(`/download/${user.id}?path=:${join(this.file.path, this.file.name)}`)
              },
            })
          }

          this.list.push({
            name: '删除文件',
            click: async() => {
              this.$confirm(`确认删除文件 ${this.file.name} ?`).then(() => {
                this.$http(
                  { method: 'delete', url: `/admin/api/${user.id}?path=${join(this.file.path, this.file.name)}` }).
                  then(() => {
                    this.$notify.success(`成功删除 ${this.file.name}`)
                    win.trigger(WindowEvent.FileDeleted, this.file)
                  }).
                  catch(err => {
                    this.$notify.error(`${this.file.name} 删除失败：${err.response.data}`)
                  })
              }).catch(() => {})
            },
          })
        }
        this.list.push(...this.$store.state.menuExtraItems)
      },
    },
  }
</script>

<style scoped lang="scss">
    .contextmenu {
        position: absolute;
        top: 0;
        left: 0;
        background: transparent;
        cursor: default;

        .contextmenu-list {
            position: absolute;
            background: white;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);

            div {
                font-size: 14px;
                padding: 5px 8px;

                &:hover {
                    background: #99a9bf;
                }
            }
        }
    }
</style>