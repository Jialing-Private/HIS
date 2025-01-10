<template>
    <div>
        <el-row :gutter="15">
            <el-col :span="15">
				<el-descriptions style="background-color: #FFFFFF; padding: 15px;" title="个人资料" :column="1" border>
					<template slot="extra">
						<el-button @click="showUpdUserWin()" type="primary" size="small">编辑</el-button>
					</template>
				    <el-descriptions-item label="用户姓名">
						{{loginUser.name}} 
						<span v-if="loginUser.gender == '男'" class="fa fa-mars-stroke"></span>
						<span v-else class="fa fa-venus"></span>
					</el-descriptions-item>
				    <el-descriptions-item label="身份证号">{{loginUser.card}}</el-descriptions-item>
				    <el-descriptions-item label="联系电话">{{loginUser.phone}}</el-descriptions-item>
				    <el-descriptions-item label="用户年龄">{{loginUser.age}}</el-descriptions-item>
				    <el-descriptions-item label="注册时间">{{loginUser.createTime}}</el-descriptions-item>
				    <el-descriptions-item label="联系地址">{{loginUser.address}}</el-descriptions-item>
				</el-descriptions>
			</el-col>
			<el-col :span="9">
				<el-card shadow="never">
					<div slot="header">
						<span class="fa fa-line-chart text-primary"></span> 科室总数
					</div>
					<div class="fater-num-panel">
						<div class="fater-num">{{ statisInfo.officeTotal }}</div>
						<div class="fater-unit">个</div>
					</div>
				</el-card>
				<el-card style="margin-top: 15px;" shadow="never">
					<div slot="header">
						<span class="fa fa-line-chart text-primary"></span> 医师总数
					</div>
					<div class="fater-num-panel">
						<div class="fater-num">{{ statisInfo.doctorTotal }}</div>
						<div class="fater-unit">位</div>
					</div>
				</el-card>
			</el-col>
		</el-row>
		
		<el-card style="margin-top: 15px;">
		    <div slot="header">
				<span class="el-icon-s-grid text-primary"></span> 预约记录
			</div>
		    <div>
				<el-row v-if="totalInfo > 0"  :gutter="15">
					<template v-for="item in pageInfos">
						<el-col :span="8">
							<div class="register-panel">
								<div class="register-icon">
									<span class="el-icon-tickets"></span>
								</div>
								<div class="register-title">
									<span class="register-doctor-name">{{ item.doctorName }}</span>
									<span class="register-doctor-desc">{{ item.doctorJob }}</span>
									<span class="register-doctor-desc">{{ item.doctorOfficeName }}</span>
								</div>
								<div class="register-detail">
									<span class="register-detail-item">预定时间：{{ item.registeTime }}</span>
									<span class="register-detail-item">挂号费用：{{ item.total }} 元</span>
								</div>
							</div>
						</el-col>
					</template>
				</el-row>
				<el-empty v-else description="暂无相关记录"></el-empty>
			</div>
		</el-card>
    
		<el-dialog title="患者信息编辑" width="700px" :visible.sync="showUpdUserFlag">
			<el-form label-width="90px" :model="userForm">
				<el-form-item label="身份证号">
				    <el-input v-model="userForm.card" 
				                placeholder="请输入身份证号…" autocomplete="off"></el-input>
				</el-form-item>
				<el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户账号">
		                    <el-input v-model="userForm.userName" 
		                                placeholder="请输入用户账号…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="用户密码">
		                    <el-input v-model="userForm.passWord" type="password"
		                                placeholder="请输入用户密码…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		        </el-row>
		        <el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户姓名">
		                    <el-input v-model="userForm.name" 
		                                placeholder="请输入用户姓名…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="联系电话">
		                    <el-input v-model="userForm.phone"
		                            placeholder="请输入联系电话…" autocomplete="off"></el-input>
		                </el-form-item>     
		            </el-col>
		        </el-row>
		        <el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户年龄">
		                    <el-input v-model="userForm.age" 
		                                placeholder="请输入用户年龄…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="用户性别">
		                    <el-radio-group v-model="userForm.gender">
		                        <el-radio label="男"></el-radio>
		                        <el-radio label="女"></el-radio>
		                    </el-radio-group>
		                </el-form-item>
		            </el-col>
		        </el-row> 
		        <el-form-item label="联系地址">
					<el-input v-model="userForm.address" type="textarea"
		                      rows="6" placeholder="请输入联系地址…" autocomplete="off"></el-input>
				</el-form-item>
		    </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdUserFlag = false">取 消</el-button>
				<el-button type="primary" @click="updLoginUser()">确 定</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<style></style>

<script>
import {
	getStatis,
	getLoginUser,
	updLoginUserInfo,
    getPageRegistes
} from "../api";
export default {
    data() {
        var checkOldPwd = async (rule, value, callback) => {
            if (value) {
                await checkUserPwd(this.$store.state.token, value).then((resp) => {
                    if (resp.code != 0) {
                        callback(new Error("原始密码输入错误"));
                    }
                });
            } else {
                callback(new Error("原始密码必须"));
            }
            callback();
        };
        var checkNewPwd = (rule, value, callback) => {
            if (!value) {
                callback(new Error("修改密码必须输入"));
            }

            callback();
        };
        var checkRePwd = (rule, value, callback) => {
            if (!value) {
                callback(new Error("确认密码必须输入"));
            }

            if (value != this.userPwd.newPwd) {
                callback(new Error("两次输入密码不一致"));
            }

            callback();
        };
        return {
			loginUser: {},
			statisInfo: {},
            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,
            showUpdUserFlag: false,
            userForm: {
				card: '',
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
    methods: {

        showUpdUserWin(){

            getLoginUser(this.$store.state.token).then(resp =>{

                this.userForm = resp.data;
				this.userForm["token"] = this.$store.state.token;
                this.showUpdUserFlag = true;
            });
        },
        updLoginUser(){

            updLoginUserInfo(this.userForm).then(() =>{

                this.$message({
                    message: '修改个人信息成功',
                    type: 'success'
                });

                this.showUpdUserFlag = false;
				
				this.$router.push("/welcome");
            });
        },
        getPageInfo(pageIndex, pageSize) {

            getPageRegistes(pageIndex, pageSize, this.$store.state.token).then(resp => {

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
    },
    mounted(){
		
		getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});
		
        this.getPageInfo(1, 12);
    }
}
</script>
