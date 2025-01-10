<template>
    <div>
		<div class="mybody">
            <el-image class="user-img" :src="require('@/assets/inhos.svg')"></el-image>

            <div class="user-info">
				<el-descriptions style="background-color: #FFFFFF; padding: 15px;" title="个人资料" :column="1" border>
					<template slot="extra">
						<el-button @click="showUpdUserWin()" type="primary" size="small">修改</el-button>
					</template>
				    <el-descriptions-item label="用户姓名">{{loginUser.name}} </el-descriptions-item>
				    <el-descriptions-item label="身份证号">{{loginUser.idNumber}}</el-descriptions-item>
				    <el-descriptions-item label="联系电话">{{loginUser.phone}}</el-descriptions-item>
				    <el-descriptions-item label="用户年龄">{{loginUser.age}}</el-descriptions-item>
				    <el-descriptions-item label="注册时间">{{loginUser.createTime}}</el-descriptions-item>
				    <el-descriptions-item label="联系地址">{{loginUser.address}}</el-descriptions-item>
				</el-descriptions>
			</div>
        
        </div>




        <el-dialog title="医师信息编辑" width="700px" :visible.sync="showUpdUserFlag">
			<el-form label-width="90px" :model="userForm">
				<el-form-item label="身份证号">
				    <el-input v-model="userForm.idNumber" 
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
			inhosPageInfos: 0,
			inhosPageIndex: 1,
			inhosPageSize: 12,
			inhosPageTotal: 0,
			inhosTotalInfo: 0,
            showUpdUserFlag: false,
			
            userForm: {
				id: '',
				idNumber: '',
                address: '',
                userName: '',
                passWord: '',
                name: '',
                gender: '',
                age: '',
                phone: '',
                type: 1,
				token: '',
            },

		
			hospitalizationFlag: false,
			showInhosDetailflag: false,
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

		showInhosDetail(){
			this.showInhosDetailflag = true;
		},


        updLoginUser(){
        
            updLoginUserInfo(this.userForm).then(() =>{
        
                this.$message({
                    message: '修改个人信息成功',
                    type: 'success'
                });
        
                this.showUpdUserFlag = false;
        		
        		location.reload();
            });
        },

        
    },

	

    mounted(){
		
		getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});
		
       
    }
}
</script>
