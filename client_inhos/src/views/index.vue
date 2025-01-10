<template>
    <el-container>
        <el-header>
            <Nav/>
        </el-header>
        <el-main class="fater-body">
            <el-row :gutter="15">
                <el-col :span="18">
                    <router-view/>
                </el-col>
                <el-col :span="6">
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>
import Nav from "../components/nav.vue";
import Bar from "../components/bar.vue";
export default {
    components: {
        Nav,
        /*Bar*/
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

        // this.toIndex();
    }
}
</script>
