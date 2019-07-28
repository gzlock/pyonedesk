<template>
    <div class="empty-user">
        <el-card>
            <div slot="header">友情提示</div>
            请到<a href="/admin">
            <el-button type="text">管理后台</el-button>
        </a>绑定 OneDrive 账号后再使用
        </el-card>
    </div>
</template>

<script>
  export default {
    name: 'empty-user-tips',
  }
</script>

<style scoped lang="scss">
    .empty-user {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>