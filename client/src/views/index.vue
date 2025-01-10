<template>
    <el-container>
        <el-header>
            <Nav/>
        </el-header>
        <el-main class="fater-body">
            <router-view/>
        </el-main>
    </el-container>
</template>

<script>
import Nav from "../components/nav.vue";

export default {
    components: {
        Nav,
    },
    data() {

        return {
            isLogin: false
        }
    },
    methods: {

        toIndex(){
            this.$router.push("/welcome");
        }
    },
    mounted(){

        if(this.$store.state.token){
                
            this.isLogin = true;
        }else{

            this.isLogin = false;
        }

        this.toIndex();
    }
}
</script>
