<template>
    <div>
		<div class="mybody">
			<el-image class="home_img"
				:src="require('@/assets/his_home.svg')">
			</el-image>

			
			
			<el-image class="welcome-box"
				:src="require('@/assets/welcome.svg')">
			</el-image>
			

			<div class="system-name"> 
				不卜庐医院信息系统
			</div>

			<!-- <div class="login-button-box" v-if="!isLogin"> -->
			<div class="login-button-box">
				<el-button @click="toPage(2)" type="primary" v-if="!isLogin"> 登 录 </el-button>
				<el-button @click="toPage(3)" type="info" v-if="!isLogin"> 注 册 </el-button>
			<!-- </div> -->
			<!-- <div class="login-button-box" v-else-if="userType==2"> -->
				<el-button @click="toPage(1)" type="primary" v-if="userType==2">挂号服务</el-button>
				<el-button @click="toPage(6)" type="primary" v-if="userType==2">住院服务</el-button>
			<!-- </div> -->
			<!-- <div class="login-button-box" v-else-if="userType==1"> -->
				<el-button @click="toPage(8)" type="primary" v-if="userType==1">个人中心</el-button>
				<el-button @click="toPage(7)" type="primary" v-if="userType==1">患者管理</el-button>

                
			</div>

            <div class="wel-contact">
                <el-row :gutter="10">
                    <el-col :span="8">
                        <el-link  href="https://gitee.com/WJL-FAna/his.git" icon="el-icon-s-promotion" type="primary">项目链接</el-link>
                    </el-col>
                    <el-col :span="8">
                        <el-link icon="el-icon-message" type="primary" href="">联系邮箱</el-link>
                    </el-col>
                    <el-col :span="8">
                        <el-link icon="el-icon-phone" type="primary" href="">联系电话</el-link>
                    </el-col>
                </el-row>
                
            </div>

            
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
				<el-button type="primary" @click="register()">确 定</el-button>
			</div>
		</el-dialog>

        
    </div>
</template>

<script>
	import {
		login,
		addPatients,
	    getPageDoctors,
		getLoginUser,
	} from "../api";
	import { mapState } from "vuex";
export default {

    data(){

        return{
			isLogin: this.$store.state.token,
            showLoginFlag: false,
            showRegisterFlag: false,
			userType: -1,
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
            },


			imgSrc:require('../assets/images/banner.jpg'),


            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
			showRegisteFlag: false,
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
				}else if(this.$store.state.token){
					this.$store.commit('setToken', this.$store.state.token);
					this.$router.push("/user");
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
			},

        getPageInfo(pageIndex, pageSize) {

            getPageDoctors(pageIndex, pageSize).then(resp => {

                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;

                this.loading = false;
            });
        },
        handleSizeChange(pageSize){

            this.getPageInfo(1, pageSize);
        },
        handleCurrentChange(pageIndex){

            this.getPageInfo(pageIndex, this.pageSize);
        },
		showRegisteWin(info){

			if(this.registerForm.token){

				this.registerForm.registerFee = info.registerFee;
				this.registerForm.doctorId = info.id;

				this.showRegisteFlag = true;
			}else{

				this.$message({
					message: '未登陆用户无法进行预约',
					type: 'warning'
				});
			}
		},
		login(){

            login(this.loginForm).then(resp =>{
                if(resp.code == 0){
                    this.$store.commit('setToken', resp.data.token);
                    this.showLoginFlag = false;
                    this.isLogin = true;
					location.reload();
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
					this.userType = this.loginUser.type;
				})} else if(sessionStorage.getItem('token')){
					getLoginUser(sessionStorage.getItem('token')).then(resp => {
						this.loginUser = resp.data;
						this.userType = this.loginUser.type;
					})} else{
						this.userType = -1;
					}
			
		},
		
	},
	mounted(){
		this.getPageInfo(1, this.pageSize);
		this.getLoginUserInfo();
	}
}
</script>