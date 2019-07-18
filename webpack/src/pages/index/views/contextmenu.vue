<template>
    <div class="contextmenu full" @click="hide" v-if="value" :style="{'z-index':$store.state.z}"
         @contextmenu.prevent="hide">
        <div :style="{left:offsetX,top:offsetY}" class="contextmenu-list">
            <div v-for="(item,i) in list" :key="i" @click="item.event">{{item.name}}</div>
        </div>
    </div>
</template>

<script>
  import { FileType } from '../js/file'

  export default {
    name: 'contextmenu',
    props: ['value', 'x', 'y', 'id', 'file'],
    data() {return { list: [] }},
    methods: {
      hide() {
        this.$emit('input', false)
      },
    },
    computed: {
      offsetX() {
        return this.x + 5 + 'px'
      },
      offsetY() {
        return this.y + 5 + 'px'
      },
    },
    watch: {
      file() {
        this.list.length = 0
        if([FileType.Folder, FileType.Text, FileType.Code, FileType.Image, FileType.Video, FileType.Audio].indexOf(
          this.file.type) > -1) {
          this.list.push({
            name: '新窗口打开',
            event: () => {this.$store.commit('createWindowFromMenu', { file: this.file })},
          })
        }
        if(this.file.type !== FileType.Folder) {
          this.list.push({
            name: '下载文件',
            event: async() => {
              alert('下载文件')
            },
          })
        }
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