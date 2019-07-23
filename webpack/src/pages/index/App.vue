<template>
    <div class="desktop full" @dragover.prevent @drop.prevent>
        <user-icon v-for="user in users" :key="user.id" :user="user"/>
        <window v-for="win in windows"
                :key="win.id" :id="win.id" :user="win.user" :file="win.file" :z="win.z" :uploads="win.uploads"
        />
        <contextmenu v-model="menu.show" :x="menu.x" :y="menu.y" :file="menu.file" :id="menu.id"/>
    </div>
</template>

<script>
  import { Index } from './preset'
  import Window from './views/window'
  import UserIcon from './views/user-icon'
  import { User } from './js/user'
  import Contextmenu from './views/contextmenu'

  export default {
    components: { Contextmenu, UserIcon, Window },
    data() {
      return {
        defaultProps: {
          children: 'children',
          label: 'label',
        },
        users: [],
      }
    },
    computed: {
      windows() {return this.$store.state.windows},
      menu() {return this.$store.state.menu},
    },
    methods: {},
    async beforeMount() {
      const res = await this.$store.dispatch('api', { url: Index.accounts })
      this.users.length = 0
      for(let key in res.data) {
        const user = res.data[key]
        const account = new User(user.id, user.name)
        this.users.push(account)
      }
      window.addEventListener('beforeunload', e => {
        if(this.$store.state.uploadingLength > 0) {
          const confirmationMessage = '\\o/';

          (e || window.event).returnValue = confirmationMessage
          return confirmationMessage
        }
      })
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