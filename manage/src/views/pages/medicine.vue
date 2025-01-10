<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				信息查询
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.drugName" placeholder="输入药品学名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.commonName" placeholder="输入药名通用名…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.price1" placeholder="输入药价最小值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.price2" placeholder="输入药价最大值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.type" placeholder="输入药品类别…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.inventory1" placeholder="输入库存量最小值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.inventory2" placeholder="输入库存量最大值…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<!-- <el-form-item label="医师职称">
						<el-select v-model="qryForm.job" placeholder="选择医师职称…" clearable>
							<el-option v-for="item in jobList" :label="item.label" :value="item.job" :key="item.job"></el-option>
						</el-select>
					</el-form-item> -->
					<!-- <el-form-item label="医师学历">
						<el-select v-model="qryForm.education" placeholder="选择医师学历…" clearable>
							<el-option v-for="item in educationList" :label="item.label" :value="item.education" :key="item.education"></el-option>
						</el-select>
					</el-form-item> -->
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
						<el-table-column align="center" prop="id" label="药品编号"></el-table-column>
						<el-table-column align="center" prop="drugName" label="药品学名"></el-table-column>
						<el-table-column align="center" prop="commonName" label="药品通用名"></el-table-column>
						<el-table-column align="center" prop="unit" label="药品单位"></el-table-column>
						<el-table-column align="center" prop="price" label="药价(元)"></el-table-column>
						<el-table-column align="center" prop="inventory" label="库存量"></el-table-column>
						<el-table-column align="center" prop="type" label="药品种类"></el-table-column>
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
			<el-form label-width="90px" :model="medicineForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="药品学名">
							<el-input v-model="medicineForm.drugName" clearable
										placeholder="请输入药品学名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药品通用名">
							<el-input v-model="medicineForm.commonName" clearable
									placeholder="请输入药品通用名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="药品单位">
							<el-input v-model="medicineForm.unit" clearable
										placeholder="请输入药品单位…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药价(元)">
							<el-input v-model="medicineForm.price" clearable
									placeholder="请输入药价…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="库存量">
							<el-input v-model="medicineForm.inventory" clearable
										placeholder="请输入库存量…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药品种类">
							<el-input v-model="medicineForm.type" clearable
										placeholder="请输入药品种类…" autocomplete="off"></el-input>
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
			<el-form label-width="90px" :model="medicineForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="药品学名">
							<el-input v-model="medicineForm.drugName" clearable
										placeholder="请输入药品学名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药品通用名">
							<el-input v-model="medicineForm.commonName" clearable
									placeholder="请输入药品通用名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="药品单位">
							<el-input v-model="medicineForm.unit" clearable
										placeholder="请输入药品单位…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药价(元)">
							<el-input v-model="medicineForm.price" clearable
									placeholder="请输入药价…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="库存量">
							<el-input v-model="medicineForm.inventory" clearable
										placeholder="请输入库存量…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="药品种类">
							<el-input v-model="medicineForm.type" clearable
										placeholder="请输入药品种类…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
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
	getPageMedicine,
	exportMedicine,
	addMedicine,
	updMedicine,
	delMedicine
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
			medicineForm: {
				id: "",
				drugName: "",
				commonName: "",
				unit: "",
				price: "",
				inventory: "",
				type: "",
			},
			qryForm: {
				drugName: "",
				commonName: "",
				type: "",
				inventory1: "",
				inventory2: "",
				price1: "",
				price2: "",
			},
        }
    },
    methods: {
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageMedicine(pageIndex, pageSize, this.qryForm.drugName, 
								this.qryForm.commonName, this.qryForm.type, this.qryForm.inventory1, this.qryForm.inventory2,
								this.qryForm.price1, this.qryForm.price2).then(resp => {

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

			this.medicineForm = {
				id: "",
				drugName: "",
				commonName: "",
				unit: "",
				price: "",
				inventory: "",
				type: "",
			};

			this.showAddFlag = true;
		},
		showUpdWin(row) {

			this.medicineForm = row;
			this.showUpdFlag = true;
		},
		addInfo() {

			addMedicine(this.medicineForm).then(resp => {

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

			updMedicine(this.medicineForm).then(resp => {

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
				
				delMedicine(id).then(resp => {
						
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
			
			exportMedicine(this.qryForm.drugName, 
								this.qryForm.commonName, this.qryForm.type, this.qryForm.inventory1, this.qryForm.inventory2,
								this.qryForm.price1, this.qryForm.price2).then(resp => {
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
