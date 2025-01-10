<template>
  <el-aside class="fater-left">
      <div class="fater-header-logo">不卜庐医院信息系统</div>
      <el-menu :default-active="this.$router.currentRoute.path" 
        background-color="#009966" text-color="#FFFFFF" active-text-color="#FFD700" router>
          <template v-for="(item, index) in menuList">
            <el-menu-item :key="index" :index="item.path">
                <span :class="item.icon"></span> 
                <span slot="title">{{ item.name }}</span>
            </el-menu-item>
          </template>
      </el-menu>
  </el-aside>
</template>

<style>
</style>

<script>

    export default{
      props: {
              menuList: []
      },
          
    }
</script>