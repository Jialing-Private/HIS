<template>
	<div class="login-container">
		<div class="login-win">
			<div class="login-body">
				<div class="login-title">
					不卜庐
				</div>
				<div class="login-form">
					<el-form :model="loginForm" :rules="rules" ref="loginForm">
						<el-form-item style="margin-bottom:30px" prop="userName">
							<el-input type="text" v-model="loginForm.userName" suffix-icon="el-icon-user-solid"
								placeholder="请输入您的账号"></el-input>
						</el-form-item>
						<el-form-item prop="passWord">
							<el-input type="password" v-model="loginForm.passWord" suffix-icon="el-icon-lock"
								placeholder="请输入您的密码"></el-input>
						</el-form-item>
						<el-form-item>
							<el-button style="margin-top: 25px; width: 100%;background-color: #009966;"
								@click="submitForm('loginForm')" type="primary">用户登录</el-button>
						</el-form-item>
					</el-form>
				</div>
			</div>
		</div>
	</div>
</template>

<style>
    .login-container {
		background-color: #009966;
		background-image: linear-gradient(to right, #009966, #339933);
		position: fixed;
		left: 0;
		top: 0;
		bottom: 0;
		right: 0;
	}
	.login-win {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 550px;
		height: 300px;
		padding: 15px;
		border-radius: 5px;
		background-image: url('../assets/bg.jpg');
		background-size: cover;
	}
	.login-body {
		position: absolute;
		right: 40px;
		top: 30px;
		width: 240px;
    }
	.login-title {
		text-align: center;
		font-size: 20px;
		font-weight: bold;
		color: #009966;
		margin-bottom: 35px;
	}
</style>
<script>
	import initMenu from "../utils/menus.js";
	import {
		login
	} from '../api/index.js'

	export default {
		data() {

			return {
				loginForm: {
					userName: '',
					passWord: '',
					flag: 0
				},
				rules: {
					userName: [{
						required: true,
						message: '用户账号必须输入',
						trigger: 'blur'
					}],
					passWord: [{
						required: true,
						message: '用户密码必须输入',
						trigger: 'blur'
					}],
				}
			}

		},
		methods: {

			submitForm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {

						login(this.loginForm).then(resp => {
							
							if(resp.code == 0){
								
								this.$store.commit('setToken', resp.data.token);
								sessionStorage.setItem("token", resp.data.token);
								initMenu(this.$router, this.$store);
								this.$router.push('/welcome');
							}else{
								this.$message({
									message: resp.msg,
									type: 'warning'
								});
							}
							
						});

					} else {

						return false;
					}
				});
			}
		}
	}
</script>
