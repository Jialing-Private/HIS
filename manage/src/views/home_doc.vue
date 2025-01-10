<template>
    <el-container>
        <Menu :menuList="this.$store.state.menus.children"></Menu>
        <el-container>
            <Nav></Nav>
            <el-main class="fater-body">
                <el-breadcrumb v-if="this.$router.currentRoute.path != '/welcome' " class="fater-body-breadcrumb">
                    <el-breadcrumb-item>
                        <el-breadcrumb-item :to="{ path: '/welcome' } ">系统首页</el-breadcrumb-item>
                    </el-breadcrumb-item>
                    <el-breadcrumb-item>{{ this.$router.currentRoute.name }}</el-breadcrumb-item>
                </el-breadcrumb>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<style>

</style>

<script>
    import Nav from "../components/nav_doc.vue";
    import Menu from "../components/menu.vue";

    export default{
        
        data(){

            return {
                
            }
        },
        methods: {

        },
        components: {
            Nav,
            Menu
        }
    }
</script>