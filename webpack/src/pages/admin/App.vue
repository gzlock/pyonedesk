<template>
    <el-container class="top-container">
        <div class="left-menu" :class="{hidden:hideMenu}">
            <el-aside width="200px">
                <div class="title">
                    <el-button circle size="mini" icon="el-icon-s-home" title="首页" @click="open('/')"></el-button>
                    账号列表
                    <el-button type="text" size="mini" icon="el-icon-plus"
                               @click.native="open({name:'add'})"></el-button>
                    <el-button type="text" size="mini" icon="el-icon-s-tools"
                               @click.native="open({name:'style_setting'})"></el-button>
                </div>
                <div class="item" v-for="(account,id) in accounts" :key="id"
                     :class="{'el-button--text':account.id===openID}" @click="open({name: 'edit', params:{id}})">
                    <template v-if="account.default">*</template>
                    {{account.name}}
                    <template v-if="!account.has_token">(未完成)</template>
                </div>
            </el-aside>
        </div>
        <el-container>
            <el-header>
                <div class="show-menu-button" v-show="routerHeader" v-if="$store.state.isMobile"
                     @click="hideMenu=false">
                    <i class="el-icon-s-unfold"></i>
                </div>
                {{routerHeader}}
            </el-header>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
  import { API } from './preset'

  export default {
    name: 'App',
    data() {
      return {
        hideMenu: false,
        routerHeader: '',
        openID: null,
      }
    },
    watch: {
      '$route': 'updateHeader',
      '$store.state.error': 'watchError',
    },
    computed: {
      accounts() {
        return this.$store.state.accounts
      },
    },
    methods: {
      updateHeader() {
        if(this.$route.meta.title)
          this.routerHeader = this.$route.meta.title
        else
          this.routerHeader = null

        if(this.$route.name === 'edit') {
          this.openID = this.$route.params.id
        }
      },
      watchError() {
        const error = this.$store.state.error
        if(error) {
          this.$alert(error.content, '⚠️' + error.title, { dangerouslyUseHTMLString: true })
        }
      },
      open(data) {
        if(data.name === 'edit') {
          this.openID = data.id
        }
        this.$router.push(data)
        this.hideMenu = true
      },
    },
    async beforeMount() {
      const res = await this.$store.dispatch('api', { url: API.accountsList })
      this.$store.commit('setAccounts', res.data)
    },
    mounted() {
      this.updateHeader()
      const clickTargets = [document.querySelector('.left-menu'), document.querySelector('.left-menu .el-aside')]
      if(this.$store.state.isMobile)
        document.querySelector('.left-menu').addEventListener('click', e => {
          if(clickTargets.indexOf(e.target) !== -1)
            this.hideMenu = true
        })
    },
  }
</script>

<style lang="scss">
    html, body, #app {
        height: 100vh;
        margin: 0;
        padding: 0;
    }

    a {
        text-decoration: none;
    }
</style>
<style scoped lang="scss">
    .left-menu, .el-aside {
        height: 100vh;
    }

    @media screen and (max-width: 700px) {
        .left-menu {
            position: absolute;
            left: 0;
            top: 0;
            width: 100vw;
            background: transparent;
            z-index: 999999;
            transition: left 1s;

            &.hidden {
                left: -100vw;
                /*.el-aside {
                    display: none;
                }*/
            }

            .el-aside {
                display: block;
                box-shadow: 0 0 5px 10px rgba(0, 0, 0, 0.1);
                background: rgba(211, 220, 230, 0.95) !important;
            }
        }
        .show-menu-button {
            margin-right: 10px;
            font-size: 20px;
            height: 100%;
            width: 60px;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            background: rgba(255, 255, 255, 0.3);
        }
        .el-header {
            padding-left: 0 !important;
        }
    }

    @media screen and (min-width: 700px) {
        .el-aside {
            width: 200px;
        }
        .show-menu-button {
            display: none
        }
    }

    .top-container {
        height: 100vh;

        .el-aside {
            background-color: #D3DCE6;
            color: #333;
        }

        .el-aside .title {
            padding: 10px;
        }

        .el-aside .item {
            padding: 10px;
            cursor: pointer;
        }

        .el-aside .item:hover {
            padding: 10px;
            background: #bbcfe6;
        }

        .el-header {
            background-color: #b3c0d1;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: left;
        }

        .el-main {
            background-color: #E9EEF3;
            color: #333;
        }

        .text-center {
            text-align: center
        }
    }
</style>