<template>
    <div class="settings-container" :class="{show}" @click.self="save">
        <a class="settings-icon" title="打开设置界面" @click="show=!show" v-if="!show"><i class="el-icon-s-tools"></i></a>
        <el-card v-if="show">
            <div slot="header" class="clearfix">全局设置</div>
            <el-form>
                <el-form-item label="同时上传文件的数量">
                    <el-input-number v-model="concurrency"/>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script>
  export default {
    name: 'settings',
    data() {
      return {
        queueConcurrency: 5,
      }
    },
    computed: {
      show: {
        set: function(value) {
          this.$store.state.settings = value
        },
        get: function() {
          return this.$store.state.settings
        },
      },
      concurrency: {
        set: function(value) {
          if(value < 1)
            value = 1
          else if(value > 11)
            value = 10
          this.queueConcurrency = value
        },
        get: function() {
          return this.queueConcurrency
        },
      },
    },
    methods: {
      save() {
        this.$store.commit('setUploadQueueConcurrency', this.queueConcurrency)
        this.show = false
      },
    },
  }
</script>

<style scoped lang="scss">
    .settings-container {
        position: absolute;
        left: 0;
        right: 0;
        z-index: 99999;

        &.show {
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .settings-icon {
            position: absolute;
            top: -10px;
            left: -30px;
            font-size: 24px;
            background: #99a9bf;
            width: 80px;
            height: 40px;
            color: white;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 5px;
            transform: rotateZ(-45deg);
            cursor: pointer;

            i {
                transform: rotateZ(45deg);
            }
        }

        .el-card {
            width: 400px;
            z-index: 1;
        }
    }
</style>