<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.name" placeholder="输入管理员姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.phone" placeholder="输入联系电话…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="管理员状态:">
						<el-radio-group v-model="qryForm.status">
							<el-radio label="正常"></el-radio>
							<el-radio label="请假"></el-radio>
							<el-radio label="离职"></el-radio>
							<el-radio label="不限"></el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="性别:">
						<el-radio-group v-model="qryForm.gender">
							<el-radio label="男"></el-radio>
							<el-radio label="女"></el-radio>
							<el-radio label="不限"></el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="类型:">
						<el-select v-model="qryForm.type1" placeholder="选择管理员类型…" clearable>
							<el-option v-for="item in typeList" :label="item.label" :value="item.type1" :key="item.type1"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" icon="el-icon-search" @click="getPageInfo(1, 10)"></el-button>
					</el-form-item>
				</el-form>
			</div>
		</el-card>
		
		<el-card shadow="never">
			<div slot="header">
				<el-button type="primary" size="mini"
						icon="el-icon-plus" @click="showAddWin()"></el-button>
				<el-button type="success" size="mini" icon="el-icon-download"
						@click="exportData">导出</el-button>
			</div>
			<div>
				<el-table v-loading="loading" stripe
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="id" label="工号"></el-table-column>
						<el-table-column align="center" prop="userName" label="账号"></el-table-column>
						<el-table-column align="center" prop="name" label="姓名"></el-table-column>
						<el-table-column align="center" prop="gender" label="性别"></el-table-column>
						<el-table-column align="center" prop="age" label="年龄"></el-table-column>
						<el-table-column align="center" prop="type1" label="类型"></el-table-column>
						<el-table-column align="center" prop="status" label="状态"></el-table-column>
						<el-table-column align="center" prop="idNumber" label="身份证号"></el-table-column>
						<el-table-column align="center" prop="phone" label="联系电话"></el-table-column>
						<el-table-column align="center" prop="address" label="联系地址" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="createTime" label="创建时间"></el-table-column>
						<el-table-column align="center" label="操作处理" fixed="right" width="150px">
							<template slot-scope="scope">
								<el-button  icon="el-icon-edit"
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button icon="el-icon-delete"
									type="danger" size="mini" @click="delInfo(scope.row.id)"></el-button>
							</template>
						</el-table-column>
				</el-table>
				<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="pageIndex" :page-sizes="[10, 20, 50]"
					:page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalInfo">
				</el-pagination>
			</div>
        </el-card>
		
		<el-dialog title="添加信息" width="750px" :visible.sync="showAddFlag">
			<el-form label-width="90px" :model="managersForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="管理员账号">
							<el-input v-model="managersForm.userName" clearable
										placeholder="请输入管理员账号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="登陆密码">
							<el-input v-model="managersForm.passWord" clearable
									type="password"	placeholder="请输入管理员登陆密码…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="管理员姓名">
							<el-input v-model="managersForm.name" clearable
										placeholder="请输入管理员姓名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="管理员年龄">
							<el-input v-model="managersForm.age" clearable
									placeholder="请输入管理员年龄…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="联系电话">
							<el-input v-model="managersForm.phone" clearable
										placeholder="请输入联系电话…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="管理员性别">
							<el-radio-group v-model="managersForm.gender">
								<el-radio label="男"></el-radio>
								<el-radio label="女"></el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
				</el-row>
				<el-form-item label="管理员类型">
					<el-select v-model="managersForm.type1" placeholder="选择管理员类型…" clearable>
						<el-option v-for="item in typeList" :label="item.label" :value="item.type1" :key="item.type1"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="身份证号">
					<el-input v-model="managersForm.idNumber" clearable
								placeholder="请输入身份证号…" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="联系地址">
					<el-input v-model="managersForm.address" type="textarea" :rows="2"
								placeholder="请输入联系地址…" autocomplete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addInfo()">确 定</el-button>
			</div>
		</el-dialog>
		
		<el-dialog title="修改信息" width="600px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="managersForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="管理员姓名">
							<el-input v-model="managersForm.name" clearable
										placeholder="请输入管理员姓名…" autocomplete="off" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="管理员年龄">
							<el-input v-model="managersForm.age" clearable
									placeholder="请输入管理员年龄…" autocomplete="off" clearable></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="联系电话">
							<el-input v-model="managersForm.phone" clearable
										placeholder="请输入联系电话…" autocomplete="off" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="管理员性别">
							<el-radio-group v-model="managersForm.gender">
								<el-radio label="男"></el-radio>
								<el-radio label="女"></el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
				<el-form-item label="管理员类型">
					<el-select v-model="managersForm.type1" placeholder="选择管理员类型…" clearable>
						<el-option v-for="item in typeList" :label="item.label" :value="item.type1" :key="item.type1"></el-option>
					</el-select>
				</el-form-item>
				</el-col>
				<el-col :span="12">
				<el-form-item label="身份证号">
					<el-input v-model="managersForm.idNumber" 
								placeholder="请输入身份证号…" autocomplete="off" clearable></el-input>
				</el-form-item>
				</el-col>
				</el-row>
				<el-form-item label="联系地址">
					<el-input v-model="managersForm.address" type="textarea" :rows="2"
								placeholder="请输入联系地址…" autocomplete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdFlag = false">取 消</el-button>
				<el-button type="primary" @click="updInfo()">确 定</el-button>
			</div>
		</el-dialog>
    </div>
</template>

<script>
import { 
	getPageManagers,
	exportManagers,
	addManagers,
	updManagers,
	delManagers
} from '../../api/index.js';

export default {
    data(){

        return {
			pageInfos: [],
			pageIndex: 1,
			pageSize: 10,
			pageTotal: 0,
			totalInfo: 0,
			loading: true,
			showAddFlag: false,
			showUpdFlag: false,
			managersForm: {
				id: "",
				userId: "",
				userName: "",
				name: "",
				gender: "",
				age: "",
				phone: "",
				address: "",
				status: "",
				createTime: "",
				idNumber: "",
				type1: "",
			},
			qryForm: {
				name: "",
				phone: "",
				gender: "",
				status: "",
				type: "",
			},
			typeList: [
				{
					type1: "超级管理员",
					label: "超级管理员",
				},
				{
					type1: "药库管理员",
					label: "药库管理员",
				}
			]
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageManagers(pageIndex, pageSize, this.qryForm.name, 
								this.qryForm.phone, this.qryForm.gender, this.qryForm.status, this.qryForm.type1).then(resp => {

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
		showAddWin() {

			this.managersForm = {
				id: "",
				userName: "",
				passWord: "",
				name: "",
				gender: "",
				age: "",
				phone: "",
				address: "",
				status: 1,
				idNumber: "",
				type1: "",
			};

			this.showAddFlag = true;
		},
		showUpdWin(row) {

			this.managersForm = row;
			this.showUpdFlag = true;
		},
		addInfo() {

			addManagers(this.managersForm).then(resp => {

				if(resp.code == 0){
					this.$message({
						message: resp.msg,
						type: 'success'
					});
					} else{
						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}

				this.getPageInfo(1, this.pageSize);

				this.showAddFlag = false;
			});
		},
		updInfo() {

			updManagers(this.managersForm).then(resp => {

				if(resp.code == 0){
					this.$message({
						message: resp.msg,
						type: 'success'
					});
					} else{
						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}

				this.getPageInfo(1, this.pageSize);

				this.showUpdFlag = false;
			});
		},
		delInfo(id) {

			this.$confirm('即将删除相关信息, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				
				delManagers(id).then(resp => {
						
					if(resp.code == 0){
					
						this.$message({
							message: resp.msg,
							type: 'success'
						});

						this.getPageInfo(1, this.pageSize);
					}else{

						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}
				});
			});
		},
		exportData() {
			
			exportManagers(this.qryForm.name, 
								this.qryForm.phone, this.qryForm.gender, this.qryForm.status, this.qryForm.type1).then(resp => {
				if(resp.code == 0){
					this.$message({
						message: resp.msg,
						type: 'success'
					});
					} else{
						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}
			});
		},
    },
    mounted(){
		
		
		
        this.getPageInfo(1, this.pageSize);
    }
}

</script>
