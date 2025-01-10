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
						<el-input v-model="qryForm.inwareId" placeholder="输入入库单号…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.type" placeholder="输入药品类型…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.producer" placeholder="输入供应商…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.handler" placeholder="输入经手人…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.recorder" placeholder="输入记录员…" autocomplete="off" clearable></el-input>
					</el-form-item>
					<el-form-item class="timeSearStyle" label="入库时间段" prop="date">
						<el-date-picker
						class="datestyle"
						v-model="qryForm.date1"
						type="date"
						clearable
						placeholder="开始日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
						<el-date-picker
						class="datestyle"
						v-model="qryForm.date2"
						type="date"
						clearable
						placeholder="结束日期"
						value-format="yyyy-MM-dd">
						</el-date-picker>
					</el-form-item>
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
						<el-table-column align="center" prop="inwareDetailId" label="入库单明细号"></el-table-column>
						<el-table-column align="center" prop="drugName" label="药品学名"></el-table-column>
						<el-table-column align="center" prop="commonName" label="药品通用名"></el-table-column>
						<el-table-column align="center" prop="unit" label="药品单位"></el-table-column>
						<el-table-column align="center" prop="num" label="入库数"></el-table-column>
						<el-table-column align="center" prop="price" label="药价(元)"></el-table-column>
						<el-table-column align="center" prop="type" label="药品种类"></el-table-column>
						<el-table-column align="center" prop="handler" label="经手人"></el-table-column>
						<el-table-column align="center" prop="recorderName" label="记录员"></el-table-column>
						<el-table-column align="center" prop="recorderType" label="记录员身份"></el-table-column>
						<el-table-column align="center" prop="plusPrice" label="明细价格"></el-table-column>
						<el-table-column align="center" prop="sumPrice" label="入库单合计"></el-table-column>
						<el-table-column align="center" prop="type" label="药品种类"></el-table-column>
						<el-table-column align="center" prop="remarks" label="备注" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" label="操作处理" fixed="right" width="150px">
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
		
		<el-dialog title="添加入库单" width="700px" :visible.sync="showAddFlag">
			<el-form  label-width="110px" :model="inWareForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="入库单号">
							<el-input v-model="inWareForm.inwareId" auto-complete = "off" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="记录员">
							<el-input v-model="inWareForm.recorderName" :disabled="true" auto-complete = "off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="入库日期">
							<el-date-picker
							class="datestyle"
							v-model="inWareForm.inwareTime"
							type="date"
							clearable
							placeholder="请选择入库日期…"
							value-format="yyyy-MM-dd"></el-date-picker>
						</el-form-item>     
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="供应商名称">
							<el-input v-model="inWareForm.producer" auto-complete = "off" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="经手人">
							<el-input v-model="inWareForm.handler" auto-complete = "off" clearable></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<div  v-for="(inWareDetail, index) in inWareForm.inWareDetail" :key="inWareForm.key">
					<el-row :gutter="65">
						<el-col :span="1" :offset="2">
							<el-button type="text" size="medium">明细{{(index+1)}}</el-button>
						</el-col>
						<el-col :span="1" >
							<el-button circle class="el-icon-delete" type="danger" size="mini" @click.prevent="removeDomain(inWareDetail)"></el-button>
						</el-col>
						<el-col :span="1">
							<el-button circle class="el-icon-plus" size="mini" type="primary" @click.prevent="addDomain"></el-button>
						</el-col>
					</el-row>
		
					<el-row :gutter="15">
						<el-col :span="12">
							<el-form-item label="药品学名">
								<el-input v-model="inWareDetail.drugName" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="12">
							<el-form-item label="药品通用名">
								<el-input v-model="inWareDetail.commonName" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row :gutter="15">
						<el-col :span="12">
							<el-form-item label="药品单位">
								<el-input v-model="inWareDetail.unit" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="12">
							<el-form-item label="药品类型">
								<el-input v-model="inWareDetail.type" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row :gutter="15">
						<el-col :span="12">
							<el-form-item label="入库数">
								<el-input v-model="inWareDetail.num" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="12">
							<el-form-item label="药品价格">
								<el-input v-model="inWareDetail.price" auto-complete = "off" clearable></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row :gutter="15">
						<el-col :span="24">
							<el-form-item label="备注">
								<el-input type="textarea" v-model="inWareDetail.remarks"
									:rows="2" placeholder="请输入备注…" autocomplete="off"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
				</div>
				<el-form-item>
					<el-button type="primary" @click="addDomain">增加检验项目</el-button>
					<el-button type="primary" @click="addInfo()">确 定</el-button>
					<el-button @click="showAddFlag = false">取 消</el-button>
				</el-form-item>
			</el-form>
		</el-dialog>
		<el-dialog title="删除入库单" width="400px" :visible.sync="showDeleteFlag">
				<el-form  label-width="0px" :model="delteForm">
					<span style="font-family: 宋体;font-size: 3ch;color: red;">是否要删除所在的入库单所有项：</span>
					<br></br>
					<el-form-item>
						<el-button @click="showDeleteFlag = false">取 消</el-button>
						<el-button type="danger" @click="deleteItem(1)">否</el-button>
						<el-button type="danger" @click="deleteItem(2)">是</el-button>
					</el-form-item>
				</el-form>
			</el-dialog>
    </div>
</template>

<script>
import { 
	getPageInWare,
	exportInWare,
	addInWare,
	delInWare,
	getLoginUser
} from '../../api/index.js';

export default {
    data(){

        return {
			loginUser: {},
			pageInfos: [],
			pageIndex: 1,
			pageSize: 10,
			pageTotal: 0,
			totalInfo: 0,
			loading: true,
			showAddFlag: false,
			showDeleteFlag: false,
			deleteId: 0,
			deleteForm: {
				id: 0,
				type: 1,
			},
			inWareForm: {
				id: 0,
				token: this.$store.state.token,
				inwareId: "",
				inwareTime: "",
				producer: "",
				handler: "",
				recorderId: 0,
				recorderName: "",
				recorderType: "",
				inWareDetail: [{
					inwareDetailId: "",
					price: 0,
					drugName: " ",
					commonName: "",
					type: "",
					remarks: " ",
					unit: "",
					num: 0,
				}]
			},
			qryForm: {
				drugName: "",
				commonName: "",
				inwareId: "",
				type: "",
				producer: "",
				handler: "",
				recorder: "",
				date1: "",
				date2: "",
			},
			DisableDatesOption: {
				disabledDate(time) {
					_this.resForm.setNowDate = _this.resForm.nowDate;
					let curDate = (new Date()).getTime();
					let pre = new Date();
					let thirtyonedays = 31 * 24 * 3600 * 1000;
					let oneMonth = curDate + thirtyonedays;
					return time.getTime() < Date.now();
				}
			},
			
        }
    },
    methods: {
		//	药物医嘱的添加删除
		removeDomain(item) {
			var index = this.inWareForm.inWareDetail.indexOf(item)
			if (index !== -1) {
			this.inWareForm.inWareDetail.splice(index, 1)
			}
		},
		
		addDomain(){
			 this.inWareForm.inWareDetail.push({
		  		value: '',
		  		key: Date.now()
			});
		},
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageInWare(pageIndex, pageSize, this.qryForm.drugName, 
								this.qryForm.commonName, this.qryForm.type, 
								this.qryForm.date1, this.qryForm.date2, this.qryForm.inwareId, 
								this.qryForm.producer, this.qryForm.handler, this.qryForm.recorder).then(resp => {

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

			this.inWareForm = {
				token: this.$store.state.token,
				id: 0,
				inwareId: "",
				inwareTime: "",
				producer: "",
				handler: "",
				inWareDetail: [{
					inwareDetailId: "",
					price: 0,
					drugName: " ",
					commonName: "",
					type: "",
					remarks: " ",
					unit: "",
					num: 0,
				}],
				recorderId: this.loginUser.id,
				recorderName: this.loginUser.name,
				recorderType: this.loginUser.type,
			},

			this.showAddFlag = true;
		},
		addInfo() {
			
			this.inWareForm.token = this.$store.state.token;
			addInWare(this.inWareForm).then(resp => {

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
					
				location.reload();

				this.getPageInfo(1, this.pageSize);

				this.showAddFlag = false;
			});
		},
		delInfo(id) {

			this.showDeleteFlag = true;
			this.deleteForm.id = id;
		},
		deleteItem(type){
			this.deleteForm.type = type;
			delInWare(this.deleteForm).then(resp =>{
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
			location.reload();
			this.getPageInfo(1, this.pageSize);
			this.showDeleteFlag = false;
		},
		exportData() {
			
			exportInWare(this.qryForm.drugName, 
								this.qryForm.commonName, this.qryForm.type, 
								this.qryForm.date1, this.qryForm.date2, this.qryForm.inwareId, 
								this.qryForm.producer, this.qryForm.handler, this.qryForm.recorder).then(resp => {
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
		getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
        this.getPageInfo(1, this.pageSize);
    }
}

</script>
