<template>
    <div >
        <div class="fater-header">
            <div class="fater-header-logo">
				<span class="fa fa-hospital-o"></span>
                不卜庐医院信息系统
            </div>
            <el-menu class="fater-header-menu" background-color="#4e60a0" mode="horizontal" >
                <el-menu-item @click="toPage(0)">系统首页</el-menu-item>
                
                <template v-if="!isLogin">
                    <el-menu-item @click="toPage(1)">科室列表</el-menu-item>
                    <el-menu-item @click="toPage(2)">用户登录</el-menu-item>
                    <el-menu-item @click="toPage(3)">用户注册</el-menu-item>
                </template>

                <template v-else-if="usertype=='2'">
                    <el-menu-item @click="toPage(9)">门诊信息</el-menu-item>
                    <el-menu-item @click="toPage(6)">住院信息</el-menu-item>
                    <el-menu-item @click="toPage(4)">个人中心</el-menu-item>
                    <el-menu-item @click="toPage(5)">退出登录</el-menu-item>
                </template>
                
                <template v-else-if="usertype=='1'">
                    <el-menu-item @click="toPage(10)">医师门诊</el-menu-item>
                    <el-menu-item @click="toPage(7)">住院患者管理</el-menu-item>
                    <el-menu-item @click="toPage(8)">个人中心</el-menu-item>
                    <el-menu-item @click="toPage(5)">退出登录</el-menu-item>
                </template>
            </el-menu>
        </div>
		
        <el-dialog title="用户登录" width="600px" :visible.sync="showLoginFlag">
			<el-form label-width="90px" :model="loginForm">
				<el-form-item label="用户账号">
					<el-input v-model="loginForm.userName" 
                                placeholder="请输入用户账号…" autocomplete="off"></el-input>
				</el-form-item>
                <el-form-item label="用户密码">
					<el-input v-model="loginForm.passWord" type="password"
                                placeholder="请输入用户密码…" autocomplete="off" @keypress.enter.native="login()"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showLoginFlag = false">取 消</el-button>
				<el-button type="primary" @click="login()">确 定</el-button>
			</div>
		</el-dialog>

        <el-dialog title="用户注册" width="700px" :visible.sync="showRegisterFlag">
			<el-form label-width="90px" :model="registerForm">
				<el-form-item label="身份证号">
				    <el-input v-model="registerForm.idNumber" 
				                placeholder="请输入身份证号…" autocomplete="off"></el-input>
				</el-form-item>
				<el-row :gutter="15">
                    <el-col :span="12">
                        <el-form-item label="用户账号">
                            <el-input v-model="registerForm.userName" 
                                        placeholder="请输入用户账号…" autocomplete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用户密码">
                            <el-input v-model="registerForm.passWord" type="password"
                                        placeholder="请输入用户密码…" autocomplete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="15">
                    <el-col :span="12">
                        <el-form-item label="用户姓名">
                            <el-input v-model="registerForm.name" 
                                        placeholder="请输入用户姓名…" autocomplete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="联系电话">
                            <el-input v-model="registerForm.phone"
                                    placeholder="请输入联系电话…" autocomplete="off"></el-input>
                        </el-form-item>     
                    </el-col>
                </el-row>
                <el-row :gutter="15">
                    <el-col :span="12">
                        <el-form-item label="用户年龄">
                            <el-input v-model="registerForm.age" 
                                        placeholder="请输入用户年龄…" autocomplete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用户性别">
                            <el-radio-group v-model="registerForm.gender">
                                <el-radio label="男"></el-radio>
                                <el-radio label="女"></el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                </el-row> 
                <el-form-item label="联系地址">
					<el-input v-model="registerForm.address" type="textarea"
                              rows="6" placeholder="请输入联系地址…" autocomplete="off"></el-input>
				</el-form-item>
            </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showRegisterFlag = false">取 消</el-button>
				<el-button type="primary" @click="register">确 定</el-button>
			</div>
		</el-dialog>
    </div>
    
    
</template>

<script>
import {
    login,
    exit,
    addPatients,
    getLoginUser,
} from "../api";
import { mapState } from "vuex";
export default {
    data() {

        return {
            isLogin: this.$store.state.token,
            usertype:'-1',
            loginUser: {},

            showLoginFlag: false,
            showRegisterFlag: false,
            loginForm: {
                userName: '',
                passWord: '',
				flag: 1
            },
            registerForm: {
				idNumber: '',
                address: '',
                userName: '',
                passWord: '',
                name: '',
                gender: '',
                age: '',
                phone: '',
                type: 2
            }
        }
    },
	computed: {
		...mapState(['token'])
	},
    methods: {

        toPage(index){
            if(index == 0){

                this.$router.push("/welcome");
            }else if(index == 1){

                this.$router.push("/list");
            }else if(index == 2){

                this.loginForm = {
                    userName: '',
                    passWord: '',
					flag: 1
                };

                this.showLoginFlag = true;
            }else if(index == 3){

                this.showRegisterFlag = true;
            }else if(index == 4){
				
				if(this.$store.state.token){
					
					this.$router.push("/user");
				}else if(sessionStorage.getItem("token")){
					
					this.$store.commit('setToken', sessionStorage.getItem("token"));
					this.$router.push("/user");;
				}else{
					
					window.location.reload();
				}
            }else if(index == 5){   

                this.$confirm("确认要退出吗？", "系统提示", {
                    confirmButtonText: "确认",
                    cancelButtonText: "取消",
                    type: "warning",
                }).then(() => {
                    exit(this.$store.state.token).then(() => {
                        this.$store.commit("clearToken");
						this.isLogin = false;
                        this.$router.push("/welcome");
						location.reload();
                    });
                });
            }else if(index == 6){
                this.$router.push("/inhos");
            }
            else if(index == 7){
                this.$router.push("/doctor_inhos");
            }
            else if(index == 8){
                this.$router.push("/doctor_info");
            }
            else if(index == 9){
                this.$router.push("/preLog")
            }
            else if(index == 10){
                this.$router.push("/opd_diagnosis")
            }

        },
        login(){

            login(this.loginForm).then(resp =>{
                this.usertype = resp.data.type;
                if(resp.code == 0){
                    this.$store.commit('setToken', resp.data.token);
                    this.showLoginFlag = false;
                    this.isLogin = true;
					
                    if(this.usertype=='2'){
                        this.$router.push("/user");
                    }
                    else if(this.usertype=='1'){
                        this.$router.push("/doctor_info");
                    }

                }else{
                    this.$message({
                        message: resp.msg,
                        type: 'warning'
                    });
                }
            });
        },
        register(){
            addPatients(this.registerForm).then(resp =>{
                if(resp.code == 0){
                    this.$message({
                        message: '注册成功',
                        type: 'success'
                    });
                    this.showRegisterFlag = false;
                }else{
                    this.$message({
                        message: resp.msg,
                        type: 'warning'
                    });
                }
            });
        },

        getLoginUserInfo(){
            if (this.$store.state.token){
                getLoginUser(this.$store.state.token).then(resp =>{
                this.loginUser = resp.data;
                this.usertype = this.loginUser.type;
                })
            }
        },

    },
        
    mounted() {
        this.getLoginUserInfo();
    },
    
}
</script>
