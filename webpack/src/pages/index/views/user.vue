<template>
    <div class="user" @dblclick="open">
        <div class="user-icon">
            <svg class="icon main-icon" aria-hidden="true">
                <use :xlink:href="'#'+icon"></use>
            </svg>
            <svg class="icon lock-icon" aria-hidden="true" v-if="user.lock">
                <use xlink:href="#py_lock"></use>
            </svg>
        </div>
        <div class="user-name">{{user.name}}</div>
    </div>
</template>

<script>
  import { User } from '../js/user'
  import { File } from '../js/file'

  export default {
    props: { user: User },
    data() {
      return {
        icon: Icons['user'],
      }
    },
    methods: {
      open() {
        this.$store.commit('createWindow', { user: this.user, file: new File('/', '/').setType(), active: true })
      },
    },
  }
</script>

<style lang="scss" scoped>
    .user {
        width: 100px;
        padding: 8px 0 0 2px;
        user-select: none;

        &:hover {
            background: rgba(233, 238, 243, 0.6);
            border-radius: 5px;
        }

        .user-icon {
            width: 100px;
            height: 60px;
            position: relative;

            svg.main-icon {
                width: 100px;
                height: 60px;
                text-align: center;
            }

            svg.lock-icon {
                position: absolute;
                width: 20px;
                height: 20px;
                bottom: 0;
                right: 0;
            }
        }

        .user-name {
            font-size: 14px;
            text-align: center;
        }

    }
</style>