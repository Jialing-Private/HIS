<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.name" placeholder="输入医师姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.phone" placeholder="输入联系电话…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.registerFeeGte" placeholder="输入挂号费最小值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.registerFeeLte" placeholder="输入挂号费最大值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="医师职称">
						<el-select v-model="qryForm.job" placeholder="选择医师职称…" clearable>
							<el-option v-for="item in jobList" :label="item.label" :value="item.job" :key="item.job"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="医师学历">
						<el-select v-model="qryForm.education" placeholder="选择医师学历…" clearable>
							<el-option v-for="item in educationList" :label="item.label" :value="item.education" :key="item.education"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="医师状态:">
						<el-radio-group v-model="qryForm.status">
							<el-radio label="正常"></el-radio>
							<el-radio label="请假"></el-radio>
							<el-radio label="离职"></el-radio>
							<el-radio label="不限"></el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="所属科室">
						<el-select style="width:100%;" v-model="qryForm.departmentId" placeholder="请选择科室" clearable>
							<el-option label="查看全部" value=""></el-option>
							<el-option v-for="(item, index) in departments" 
								:key="index" :label="item.name" :value="item.id"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="性别:">
						<el-radio-group v-model="qryForm.gender">
							<el-radio label="男"></el-radio>
							<el-radio label="女"></el-radio>
							<el-radio label="不限"></el-radio>
						</el-radio-group>
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
						<el-table-column align="center" prop="registerFee" label="挂号费"></el-table-column>
						<el-table-column align="center" prop="gender" label="性别"></el-table-column>
						<el-table-column align="center" prop="age" label="年龄"></el-table-column>
						<el-table-column align="center" prop="status" label="状态"></el-table-column>
						<el-table-column align="center" prop="idNumber" label="身份证号"></el-table-column>
						<el-table-column align="center" prop="education" label="学历"></el-table-column>
						<el-table-column align="center" prop="job" label="职称"></el-table-column>
						<el-table-column align="center" prop="departmentName" label="所属科室"></el-table-column>
						<el-table-column align="center" prop="phone" label="联系电话"></el-table-column>
						<el-table-column align="center" prop="address" label="联系地址" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="speciality" label="专长" :show-overflow-tooltip="true"></el-table-column>
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
			<el-form label-width="90px" :model="doctorsForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医师账号">
							<el-input v-model="doctorsForm.userName" clearable
										placeholder="请输入医师账号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="登陆密码">
							<el-input v-model="doctorsForm.passWord" clearable
									type="password"	placeholder="请输入医师登陆密码…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医师姓名">
							<el-input v-model="doctorsForm.name" clearable
										placeholder="请输入医师姓名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="医师年龄">
							<el-input v-model="doctorsForm.age" clearable
									placeholder="请输入医师年龄…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="联系电话">
							<el-input v-model="doctorsForm.phone" clearable
										placeholder="请输入联系电话…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="医师性别">
							<el-radio-group v-model="doctorsForm.gender">
								<el-radio label="男"></el-radio>
								<el-radio label="女"></el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医师职称">
							<el-select v-model="doctorsForm.job" placeholder="选择医师职称…" clearable>
								<el-option v-for="item in jobList" :label="item.label" :value="item.job" :key="item.job"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="医师学历">
							<el-select v-model="doctorsForm.education" placeholder="选择医师学历…" clearable>
								<el-option v-for="item in educationList" :label="item.label" :value="item.education" :key="item.education"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="挂号费用">
							<el-input v-model="doctorsForm.registerFee" clearable
										placeholder="请输入医师挂号费用…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="所属科室">
							<el-select style="width:100%;" v-model="doctorsForm.departmentId" placeholder="请选择科室">
								<el-option label="查看全部" value=""></el-option>
								<el-option v-for="(item, index) in departments" 
									:key="index" :label="item.name" :value="item.id"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="身份证号">
							<el-input v-model="doctorsForm.idNumber" clearable
									placeholder="请输入身份证号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="联系地址">
							<el-input v-model="doctorsForm.address" type="textarea" :rows="2"
									placeholder="请输入医师联系地址…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-form-item label="专长描述">
					<el-input v-model="doctorsForm.speciality" type="textarea" :rows="4"
							placeholder="请输入医师专长描述…" autocomplete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addInfo()">确 定</el-button>
			</div>
		</el-dialog>
		
		<el-dialog title="修改信息" width="600px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="doctorsForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医师姓名">
							<el-input v-model="doctorsForm.name" 
										placeholder="请输入医师姓名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="医师年龄">
							<el-input v-model="doctorsForm.age" 
									placeholder="请输入医师年龄…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医师职称">
							<el-select v-model="doctorsForm.job" placeholder="选择医师职称…" clearable>
								<el-option v-for="item in jobList" :label="item.label" :value="item.job" :key="item.job"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="医师学历">
							<el-select v-model="doctorsForm.education" placeholder="选择医师学历…" clearable>
								<el-option v-for="item in educationList" :label="item.label" :value="item.education" :key="item.education"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
				<el-form-item label="医师状态:">
					<el-radio-group v-model="doctorsForm.status">
						<el-radio label="正常"></el-radio>
						<el-radio label="请假"></el-radio>
						<el-radio label="离职"></el-radio>
					</el-radio-group>
				</el-form-item>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="挂号费用">
							<el-input v-model="doctorsForm.registerFee" 
										placeholder="请输入医师挂号费用…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="所属科室">
							<el-select style="width:100%;" v-model="doctorsForm.departmentId" placeholder="请选择科室">
								<el-option label="查看全部" value=""></el-option>
								<el-option v-for="(item, index) in departments" 
									:key="index" :label="item.name" :value="item.id"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="身份证号">
							<el-input v-model="doctorsForm.idNumber" clearable
									placeholder="请输入身份证号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="联系地址">
							<el-input v-model="doctorsForm.address" type="textarea" :rows="2"
									placeholder="请输入医师联系地址…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-form-item label="专长描述">
					<el-input v-model="doctorsForm.speciality" type="textarea" :rows="6"
							placeholder="请输入医师专长描述…" autocomplete="off"></el-input>
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
	getAllDepartments,
	getPageDoctors,
	exportDoctors,
	addDoctors,
	updDoctors,
	delDoctors
} from '../../api/index.js';

export default {
    data(){

        return {
			departments: [],
			pageInfos: [],
			pageIndex: 1,
			pageSize: 10,
			pageTotal: 0,
			totalInfo: 0,
			loading: true,
			showAddFlag: false,
			showUpdFlag: false,
			doctorsForm: {
				id: "",
				userId: "",
				userName: "",
				passWord: "",
				name: "",
				gender: "",
				age: "",
				phone: "",
				type: 1,
				education: "",
				job: "",
				speciality: "",
				registerFee: "",
				departmentId: "",
				address: "",
				status: "",
				idNumber: "",
			},
			qryForm: {
				name: "",
				phone: "",
				registerFeeGte: "",
				registerFeeLte: "",
				education: "",
				job: "",
				departmentId: "",
				gender: "",
				status: "",
			},
			educationList: [
				{
					education: "博士",
					label: "博士",
				},
				{
					education: "硕士",
					label: "硕士",
				},
				{
					education: "本科",
					label: "本科",
				},
				{
					education: "专科",
					label: "专科"
				},
				{
					education: "高中",
					label: "高中"
				},
				{
					education: "中等职业教育",
					label: "中等职业教育"
				},
				{
					education: "初中",
					label: "初中"
				},
				{
					education: "小学",
					label: "小学"
				},
			],
			jobList: [
				{
					job: "医士",
					label: "医士",
				},
				{
					job: "医师",
					label: "医师",
				},
				{
					job: "住院医师",
					label: "住院医师",
				},
				{
					job: "主治医师",
					label: "主治医师",
				},
				{
					job: "副主任医师",
					label: "副主任医师",
				},
				{
					job: "主任医师",
					label: "主任医师",
				},
			]
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageDoctors(pageIndex, pageSize, this.qryForm.name, 
								this.qryForm.phone, this.qryForm.gender, this.qryForm.education, this.qryForm.job,
								this.qryForm.registerFeeGte, this.qryForm.registerFeeLte,
								this.qryForm.departmentId,  this.qryForm.status).then(resp => {

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

			this.doctorsForm = {
				id: "",
				userId: "",
				userName: "",
				name: "",
				gender: "",
				age: "",
				phone: "",
				type: 1,
				education: "",
				job: "",
				speciality: "",
				registerFee: "",
				departmentId: "",
				departmentName: "",
				status: 1,
				idNumber: "",
			};

			this.showAddFlag = true;
		},
		showUpdWin(row) {

			this.doctorsForm = row;
			this.showUpdFlag = true;
		},
		addInfo() {

			addDoctors(this.doctorsForm).then(resp => {

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

			updDoctors(this.doctorsForm).then(resp => {

				if(resp.code == 0){
					this.$message({
						message: resp.msg,
						type: 'success'
					});
					this.getPageInfo(1, this.pageSize);
					} else{
						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}				

				this.showUpdFlag = false;
			});
		},
		delInfo(id) {

			this.$confirm('即将删除相关信息, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				
				delDoctors(id).then(resp => {
						
					if(resp.code == 0){
					
						this.$message({
							message: resp.msg,
							type: 'success'
						});
						this.getPageInfo(1, this.pageSize);
						} else {

						this.$message({
							message: resp.msg,
							type: 'warning'
						});
					}
					
				});
			});
		},
		exportData() {
			
			exportDoctors(this.qryForm.name, 
								this.qryForm.phone, this.qryForm.gender, this.qryForm.education, this.qryForm.job,
								this.qryForm.registerFeeGte, this.qryForm.registerFeeLte,
								this.qryForm.departmentId,  this.qryForm.status).then(resp => {
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
		
		getAllDepartments().then(resp =>{
			
			this.departments = resp.data;
		});
		
        this.getPageInfo(1, this.pageSize);
    }
}

</script>
