<template>
    <div class="loading">
        读取中
    </div>
</template>

<script>
  export default {
    name: 'window-loading',
  }
</script>

<style scoped lang="scss">
    .loading {
        width: 100%;
        height: 100%;
        position: absolute;
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #99a9bf;
        background: white;
    }
</style>