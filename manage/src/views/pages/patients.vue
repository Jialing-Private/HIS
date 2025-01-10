<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.name" placeholder="输入患者姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.phone" placeholder="输入联系电话…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.address" placeholder="输入患者联系地址…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="性别:">
						<el-radio-group v-model="qryForm.gender">
							<el-radio label="男"></el-radio>
							<el-radio label="女"></el-radio>
							<el-radio label="不限"></el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="病人账号状态:">
						<el-select v-model="qryForm.status" placeholder="选择病人账号状态…" clearable>
							<el-option v-for="item in statusList" :label="item.label" :value="item.status" :key="item.status"></el-option>
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
				<el-button type="success" size="mini" icon="el-icon-download"
						@click="exportData">导出</el-button>
			</div>
			<div>
				<el-table v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="userName" label="患者账号"></el-table-column>
						<el-table-column align="center" prop="name" label="患者姓名"></el-table-column>
						<el-table-column align="center" prop="gender" label="患者性别"></el-table-column>
						<el-table-column align="center" prop="phone" label="联系电话"></el-table-column>
						<el-table-column align="center" prop="idNumber" label="身份证号"></el-table-column>
						<el-table-column align="center" prop="address" label="联系地址"></el-table-column>
						<el-table-column align="center" prop="status" label="患者账号状态"></el-table-column>
						<el-table-column align="center" prop="createTime" label="注册时间"></el-table-column>
						<el-table-column align="center" label="操作处理">
							<template slot-scope="scope">
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
    </div>
</template>

<script>
import { 
	getPagePatients,
	delPatients,
	exportPatients
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
			patientsForm: {
				id: "",
				address: "",
				idNumber: "",
				status: "",
				gender: "",
				name: "",
				userName: "",
				address: "",
				createTime: "",
				phone: "",
				age: "",
				updateTime: "",
			},
			qryForm: {
				name: "",
				phone: "",
				address: "",
				gender: "",
				status: "",
			},
			statusList: [
				{
					status: "正常",
					label: "正常",
				},
				{
					status: "账号已注销",
					label: "账号已注销",
				},
				{
					status: "不限",
					label: "不限",
				}
			],
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPagePatients(pageIndex, pageSize, this.qryForm.name, 
								this.qryForm.phone, this.qryForm.address, this.qryForm.status, this.qryForm.gender).then(resp => {

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

			this.patientsForm = {
				id: "",
				address: "",
				idNumber: "",
			};

			this.showAddFlag = true;
		},
		delInfo(id) {

			this.$confirm('即将删除相关信息, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				
				delPatients(id).then(resp => {
						
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
				
				this.getPageInfo(1, this.pageSize);
			});
		},
		exportData() {
			
			exportPatients(this.qryForm.name, this.qryForm.phone, this.qryForm.address,
			 this.qryForm.status, this.qryForm.gender).then(resp => {
				if(resp.code == 0){
					this.$message({
						message: resp.msg,
						type: 'success'
					});
					} else {
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
