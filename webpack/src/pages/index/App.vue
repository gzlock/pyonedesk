<template>
    <div class="desktop full">
        <user-icon v-for="user in users" :key="user.id" :user="user" @dblclick="createRootWindow(user)"/>
        <window v-for="(win,id) in windows"
                :key="id" :id="id" :user="win.user" :file="win.file" :z="win.z"
                @createWindow="createWindow"
                @close="closeWindow"
                @focus="setTop"
                @contextmenu="contextmenu"/>
        <contextmenu v-model="menu.show" :x="menu.x" :y="menu.y" :file="menu.file"/>
    </div>
</template>

<script>
  import { Index } from './preset'
  import Window from './views/window'
  import UserIcon from './views/user-icon'
  import '@/assets/global.scss'
  import { User } from './js/user'
  import { File } from './js/file'
  import { sortBy } from 'lodash'
  import Contextmenu from '@/pages/index/views/contextmenu'

  export default {
    components: { Contextmenu, UserIcon, Window },
    data() {
      return {
        defaultProps: {
          children: 'children',
          label: 'label',
        },
        users: [],
        windows: {},
        menu: { show: false, x: 0, y: 0, id: null, file: null },
      }
    },
    methods: {
      createRootWindow(user) {
        this.createWindow(user, new File('/', '/'))
      },
      createWindow(user, file, active = false) {
        const id = Date.now().toString(32)
        this.$set(this.windows, id, { id, user, file, z: this.$store.state.z })
        this.$store.state.z++
        if(active)
          this.$store.state.activeID = id
      },
      createWindowFromMenu(file) {
        console.log('createWindowFromMenu', file)
        this.createWindow(this.windows[this.menu.id].user, file, true)
      },
      clearWindow() {
        this.windows = {}
      },
      closeWindow(id) {
        console.log('关闭窗口', id)
        this.$delete(this.windows, id)
      },
      setTop(id) {
        console.log('setTop', id)
        this.$store.state.activeID = id
        this.windows[id].z = this.$store.state.z
        const sorted = sortBy(this.windows, 'z')
        sorted.forEach(win => {
          const index = sorted.indexOf(win)
          win.z = index + 1
        })
        this.$store.state.z = sorted.length + 1
      },
      contextmenu(e, id, file) {
        console.log('右键', e, id, file)
        this.menu.show = true
        this.menu.x = e.clientX
        this.menu.y = e.clientY
        this.menu.file = file
        this.menu.id = id
      },
    },
    async beforeMount() {
      this.$store.state.menuCallback = this.contextmenu
      this.$store.state.createWindowFromMenu = this.createWindowFromMenu
      const res = await this.$store.dispatch('api', { url: Index.accounts })
      this.users.length = 0
      for(let key in res.data) {
        const user = res.data[key]
        const account = new User(user.id, user.name)
        this.users.push(account)
      }
    },
  }
</script>

<style scoped lang="scss">
    @import "@/assets/global.scss";

    .desktop {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        overflow: hidden;
        position: absolute;

        .user {
            margin: $windowPaddingLeft 0 0 $windowPaddingLeft;
        }
    }
</style>