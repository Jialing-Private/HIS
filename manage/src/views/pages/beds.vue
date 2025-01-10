<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.bid" placeholder="输入床位编号…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.pricegte" placeholder="输入价格下限…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.pricelte" placeholder="输入价格上限…" autocomplete="off"> clearable</el-input>
					</el-form-item>
					<el-form-item >
						<el-select v-model="qryForm.type" placeholder="选择床位床位类别…" clearable>
							<el-option v-for="item in typeList" :label="item.label" :value="item.type" :key="item.type"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item >
						<el-select v-model="qryForm.status" placeholder="选择床位状态…" clearable>
							<el-option v-for="item in statusList" :label="item.label" :value="item.status" :key="item.status"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="所属科室">
						<el-select style="width:100%;" v-model="qryForm.departmentId" placeholder="请选择科室">
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
				<el-button type="primary" size="mini"
						icon="el-icon-plus" @click="showAddWin()"></el-button>
				<el-button type="success" size="mini" icon="el-icon-download"
						@click="exportData">导出</el-button>
			</div>
			<div>
				<el-table v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="bid" label="床位编号"></el-table-column>
						<el-table-column align="center" prop="type" label="床位类别"></el-table-column>
						<el-table-column align="center" prop="departmentName" label="床位所属科室"></el-table-column>
						<el-table-column align="center" prop="status" label="床位状态"></el-table-column>
						<el-table-column align="center" prop="price" label="床位价格"></el-table-column>
						<el-table-column align="center" prop="createTime" label="创建时间"></el-table-column>
						<el-table-column align="center" label="操作处理"  fixed="right" width="150px">
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
			<el-form label-width="90px" :model="bedsForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="床位编号">
							<el-input v-model="bedsForm.bid" 
										placeholder="请输入床位编号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="床位价格">
							<el-input v-model="bedsForm.price" 
									placeholder="请输入床位价格…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="床位类别">
							<el-select v-model="bedsForm.type" placeholder="选择床位床位类别…" clearable>
								<el-option v-for="item in typeList" :label="item.label" :value="item.type" :key="item.type"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="所属科室">
							<el-select style="width:100%;" v-model="bedsForm.departmentId" placeholder="请选择科室">
								<el-option label="查看全部" value=""></el-option>
								<el-option v-for="(item, index) in departments" 
									:key="index" :label="item.name" :value="item.id"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addInfo()">确 定</el-button>
			</div>
		</el-dialog>
		
		<el-dialog title="修改信息" width="600px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="bedsForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="床位编号">
							<el-input v-model="bedsForm.bid" 
										placeholder="请输入床位编号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="床位价格">
							<el-input v-model="bedsForm.price" 
									placeholder="请输入床位价格…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="床位类别">
							<el-select v-model="bedsForm.type" placeholder="选择床位床位类别…" clearable>
								<el-option v-for="item in typeList" :label="item.label" :value="item.type" :key="item.type"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="所属科室">
							<el-select style="width:100%;" v-model="bedsForm.departmentId" placeholder="请选择科室">
								<el-option label="查看全部" value=""></el-option>
								<el-option v-for="(item, index) in departments" 
									:key="index" :label="item.name" :value="item.id"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
				<el-form-item label="床位状态">
					<el-select v-model="bedsForm.status" placeholder="选择床位状态…" clearable>
						<el-option v-for="item in statusList" :label="item.label" :value="item.status" :key="item.status"></el-option>
					</el-select>
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
	getPageBeds,
	exportBeds,
	addBeds,
	updBeds,
	delBeds,
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
			bedsForm: {
				id: "",
				bid: "",
				type: "",
				price: "",
				status: "",
				createTime: "",
				updateTime: "",
				departmentId: "",
			},
			qryForm: {
				bid: "",
				pricegte: "",
				pricelte: "",
				type: "",
				status: "",
				departmentId: "",
			},
			statusList: [
				{
					status: "查看全部",
					label: "查看全部",
				},
				{
					status: "停用",
					label: "停用",
				},
				{
					status: "正常",
					label: "正常",
				},
				{
					status: "使用中",
					label: "使用中",
				},
				{
					status: "占用中",
					label: "占用中",
				}
			],
			typeList: [
				{
					type: "查看全部",
					label: "查看全部",
				},
				{
					type: "双摇床",
					label: "双摇床",
				}
			]
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageBeds(pageIndex, pageSize, this.qryForm.bid, this.qryForm.pricegte, this.qryForm.pricelte,
								this.qryForm.type, this.qryForm.status, this.qryForm.departmentId).then(resp => {

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

			this.bedsForm = {
				id: "",
				bid: "",
				type: "",
				price: "",
				status: 1,
				createTime: "",
				updateTime: "",
				departmentId: "",
			};

			this.showAddFlag = true;
		},
		showUpdWin(row) {

			this.bedsForm = row;
			this.showUpdFlag = true;
		},
		addInfo() {

			addBeds(this.bedsForm).then(resp => {

				this.$message({
					message: resp.msg,
					type: 'success'
				});

				this.getPageInfo(1, this.pageSize);

				this.showAddFlag = false;
			});
		},
		updInfo() {

			updBeds(this.bedsForm).then(resp => {

				this.$message({
					message: resp.msg,
					type: 'success'
				});

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
				
				delBeds(id).then(resp => {
						
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
			
			exportBeds(this.qryForm.bid, this.qryForm.pricegte, this.qryForm.pricelte,
								this.qryForm.type, this.qryForm.status, this.qryForm.departmentId).then(resp => {
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
