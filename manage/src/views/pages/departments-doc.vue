<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item label="科室编号">
						<el-input v-model="qryForm.did" placeholder="输入科室编号…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="科室名称">
						<el-input v-model="qryForm.name" placeholder="输入科室名称…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item label="科室类型">
						<el-select v-model="qryForm.status" placeholder="选择科室类型…" clearable>
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
				<el-table v-loading="loading"  :id="departmentsTable" stripe
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="did" label="科室编号"></el-table-column>
						<el-table-column align="center" prop="name" label="科室名称"></el-table-column>
						<el-table-column align="center" prop="status" label="科室类型"></el-table-column>
						<el-table-column align="center" prop="createTime" label="创建时间"></el-table-column>
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
	getPageDepartments,
	updDepartments,
	exportDepartments,
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
			departmentsForm: {
				id: "",
				did: "",
				name: "",
				describe: "",
				status: "",
			},
			qryForm: {
				did: "",
				name: "",
				status: "",
			},
			selectedStatus: "",
			statusList: [
				{
					status: 1,
					label: "门诊部",
				},
				{
					status: 2,
					label: "住院部",
				},
				{
					status: 3,
					label: "其他",
				},
				{
					status: 0,
					label: "已停用"
				},
			]
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageDepartments(pageIndex, pageSize, this.qryForm.did, this.qryForm.name, this.qryForm.status).then(resp => {

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

			this.departmentsForm = {
				id: "",
				did: "",
				name: "",
				describe: "",
				status: "",
			};

			this.showAddFlag = true;
		},
		showUpdWin(row) {

			this.departmentsForm = row;
			this.showUpdFlag = true;
		},
		addInfo() {

			addDepartments(this.departmentsForm).then(resp => {

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

			updDepartments(this.departmentsForm).then(resp => {

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
				
				delDepartments(id).then(resp => {
						
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
			
			exportDepartments(this.qryForm.did, this.qryForm.name, this.qryForm.status).then(resp => {
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
