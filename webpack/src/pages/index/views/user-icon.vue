<template>
    <div class="user" @dblclick="$emit('dblclick',user)">
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

  export default {
    props: { user: User, icon: Icons['user'] },
    computed: {},
  }
</script>

<style lang="scss" scoped>
    .user {
        user-select: none;

        .user-icon {
            position: relative;
            width: 60px;
            height: 60px;

            .main-icon {
                width: 100%;
                height: 100%;
            }

            .lock-icon {
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