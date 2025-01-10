<template>
	<div class="fater-body-show">
		<el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item>
						<el-input v-model="qryForm.doctorName" placeholder="输入医师姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item>
						<el-input v-model="qryForm.patientName" placeholder="输入患者姓名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item>
						<el-input v-model="qryForm.bedBid" placeholder="输入床位编号…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item>
						<el-select v-model="qryForm.status" placeholder="选择住院状态…" clearable>
							<el-option v-for="item in statusList" :label="item.label" :value="item.status" :key="item.status"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="住院科室" clearable>
						<el-select style="width:100%;" v-model="qryForm.departmentId" placeholder="请选择科室" clearable>
							<el-option label="查看全部" value=""></el-option>
							<el-option v-for="(item, index) in departments" 
								:key="index" :label="item.name" :value="item.id"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item class="timeSearStyle" label="入院时间范围" prop="date" clearable>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.startTime1"
						type="date"
						clearable
						placeholder="开始日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.startTime2"
						type="date"
						clearable
						placeholder="结束日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
					</el-form-item>
					<el-form-item class="timeSearStyle" label="出院时间范围" prop="date" clearable>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.endTime1"
						type="date"
						clearable
						placeholder="开始日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.endTime2"
						type="date"
						clearable
						placeholder="结束日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
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
					<el-table-column align="center" prop="departmentName" label="住院科室"></el-table-column>
					<el-table-column align="center" prop="status" label="住院状态"></el-table-column>
					<el-table-column align="center" prop="patientPhone" label="患者联系电话"></el-table-column>
					<el-table-column align="center" prop="startTime" label="住院开始时间"></el-table-column>
					<el-table-column align="center" prop="endTime" label="出院时间"></el-table-column>
					<el-table-column align="center" prop="duringTime" label="住院时长"></el-table-column>
					
					<el-table-column align="center" prop="doctorName" label="医师姓名"></el-table-column>
					<el-table-column align="center" prop="doctorGender" label="医师性别"></el-table-column>
					<el-table-column align="center" prop="doctorDepartmentName" label="医师所属科室"></el-table-column>
					<el-table-column align="center" prop="doctorRegisterFee" label="挂号费用"></el-table-column>
					
					<el-table-column align="center" prop="bedBid" label="床位编号"></el-table-column>
					<el-table-column align="center" prop="bedType" label="床位类型"></el-table-column>
					<el-table-column align="center" prop="bedPrice" label="床位价格"></el-table-column>
					
					<el-table-column align="center" prop="doctorName" label="预约医师"></el-table-column>
					<el-table-column align="center" prop="registerTime" label="预约时间"></el-table-column>
					
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
		delHospitalizationLogs,
		getPageHospitalizationLogs,
		exportHospitalizationLogs,
		getInHosDepartments,
		// updRegistes,
	} from '../../api/index.js';

	export default {
		data() {

			return {
				departments: [],
				pageInfos: [],
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
					departmentId: "",
					startTime1: "",
					startTime2: "",
					endTime1: "",
					endTime2: "",
					bedBid: "",
					status: "",
				},
				statusList: [
					{
						label: "待入院",
						status: 1,
					},
					{
						label: "已出院/患者拒绝入院",
						status: 0,
					},
					{
						label: "已入院",
						status: 2,
					},
					{
						label: "待出院",
						status: 3,
					}
				],
			}
		},
		methods: {

			getPageInfo(pageIndex, pageSize) {

				getPageHospitalizationLogs(pageIndex, pageSize, this.qryForm.token, this.qryForm.doctorName,
				this.qryForm.patientName, this.qryForm.departmentId, this.qryForm.startTime1, 
				this.qryForm.startTime2, this.qryForm.endTime1, this.qryForm.endTime2, this.qryForm.bedBid, this.qryForm.status).then(resp => {

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
					
					delHospitalizationLogs(id).then(resp => {
							
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
					
				exportHospitalizationLogs(this.qryForm.token, this.qryForm.doctorName,
				this.qryForm.patientName, this.qryForm.departmentId, this.qryForm.startTime1, 
				this.qryForm.startTime2, this.qryForm.endTime1, this.qryForm.endTime2, 
				this.qryForm.bedBid, this.qryForm.status).then(resp => {
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
			getInHosDepartments().then(resp =>{
				
				this.departments = resp.data;
			});

			this.getPageInfo(1, this.pageSize);
		}
	}
</script>
