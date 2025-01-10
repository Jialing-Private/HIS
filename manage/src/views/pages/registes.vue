<template>
	<div class="fater-body-show">
		<el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item label="医师姓名">
						<el-input v-model="qryForm.doctorName" placeholder="输入医师姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="患者姓名">
						<el-input v-model="qryForm.patientName" placeholder="输入患者姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item class="timeSearStyle" label="预约时间" prop="date" clearable>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.value1"
						type="date"
						clearable
						placeholder="开始日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.value2"
						type="date"
						clearable
						placeholder="结束日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
					</el-form-item>
					<el-form-item label="预约科室" clearable>
						<el-select style="width:100%;" v-model="qryForm.departmentId" placeholder="请选择科室" clearable>
							<el-option label="查看全部" value=""></el-option>
							<el-option v-for="(item, index) in departments" 
								:key="index" :label="item.name" :value="item.id"></el-option>
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
				<el-table v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" stripe
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
					<el-table-column align="center" type="index"></el-table-column>
					<el-table-column align="center" prop="patientName" label="患者姓名"></el-table-column>
					<el-table-column align="center" prop="patientGender" label="患者性别"></el-table-column>
					<el-table-column align="center" prop="patientAge" label="患者年龄"></el-table-column>
					<el-table-column align="center" prop="patientPhone" label="患者联系电话"></el-table-column>
					<el-table-column align="center" prop="doctorName" label="预约医师"></el-table-column>
					<el-table-column align="center" prop="departmentName" label="预约门诊"></el-table-column>
					<el-table-column align="center" prop="registerFee" label="挂号费用"></el-table-column>
					<el-table-column align="center" prop="registerTime" label="预约时间"></el-table-column>
					<el-table-column align="center" prop="status2" label="当前状态"></el-table-column>
					<el-table-column align="center" prop="createTime" label="创建时间"></el-table-column>	
					<el-table-column align="center" label="操作处理" fixed="right" width="80px">
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
		getAllDepartments,
		delRegistes,
		getPageRegistes,
		exportRegistes,
		// updRegistes,
	} from '../../api/index.js';

	export default {
		data() {

			return {
				pageInfos: [],
				departments: [],
				pageIndex: 1,
				pageSize: 10,
				pageTotal: 0,
				totalInfo: 0,
				loading: true,
				showAddFlag: false,
				qryForm: {
					token: this.$store.state.token,
					doctorName: "",
					patientName: "",
					value1: "",
					value2: "",
					departmentId: "",
				},
			}
		},
		methods: {

			getPageInfo(pageIndex, pageSize) {

				getPageRegistes(pageIndex, pageSize, this.qryForm.token, 
				this.qryForm.doctorName, this.qryForm.patientName, 
				this.qryForm.value1, this.qryForm.value2, 
				this.qryForm.departmentId).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.pageTotal = resp.data.pageTotal;
					this.totalInfo = resp.data.count;

					this.loading = false;
				});
			},
			handleSizeChange(pageSize) {

				this.getPageInfo(1, pageSize);
			},
			handleCurrentChange(pageIndex) {

				this.getPageInfo(pageIndex, this.pageSize);
			},
			delInfo(id) {
			
				this.$confirm('即将删除相关信息, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					
					delRegistes(id).then(resp => {
							
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
				
				exportRegistes(this.qryForm.token, 
				this.qryForm.doctorName, this.qryForm.patientName, 
				this.qryForm.value1, this.qryForm.value2, 
				this.qryForm.departmentId).then(resp => {
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
		mounted() {
			getAllDepartments().then(resp =>{
				
				this.departments = resp.data;
			});

			this.getPageInfo(1, this.pageSize);
		}
	}
</script>
