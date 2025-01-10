<template>
    <div class="mybody">
		<div class="patient-info-cards">
			<el-card style="margin-bottom: 15px;">
				<div slot="header">
					<span class="el-icon-s-grid"></span>  住院患者列表
				</div>
				
				<div>
					<el-table v-loading="loading" 
						element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
						element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
							<el-table-column align="center" type="index"></el-table-column>
							
							<el-table-column align="center" prop="patientName" label="患者姓名"></el-table-column>
							<el-table-column align="center" prop="patientGender" label="患者性别"></el-table-column>
							<el-table-column align="center" prop="patientAge" label="患者年龄"></el-table-column>
							<el-table-column align="center" prop="patientPhone" label="联系电话"></el-table-column>
							<el-table-column align="center" prop="departmentName" label="住院科室"></el-table-column>
							
							
							<el-table-column sortable align="center" prop="hospitalizationStartTime" label="入院时间"></el-table-column>
							
							<el-table-column align="center" prop="status" label="状态" 
							:filters="[{text: '待入院', value: '待入院'}, {text: '已入院', value: '已入院'}, {text: '待出院', value: '待出院'}]"
      						:filter-method="filterHandler">
							</el-table-column>
							
							<el-table-column align="center" label="操作" fixed="right" width="200px">
								<template slot-scope="scope">
									<el-button type="text" @click="addMedcalAdvice(scope.$index, 1)" v-show="scope.row.status=='已入院'">开药</el-button>
									<el-button type="text" @click="addMedcalAdvice(scope.$index, 2)" v-show="scope.row.status=='已入院'">化验</el-button>
									<el-button type="text" @click="outhospital(scope.row.id)"  v-show="scope.row.status=='已入院'">办理出院</el-button>
								</template>
							</el-table-column>
					</el-table>
					<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
						@current-change="handleCurrentChange" :current-page="pageIndex" :page-sizes="[10, 20, 50]"
						:page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalInfo">
					</el-pagination>
				</div>
        	</el-card>



			<el-card style="margin-bottom: 15px;">
				<div slot="header">
					<span class="el-icon-s-grid"></span>  历史医嘱记录查询
				</div>
				
				<el-row :gutter="60">
					<el-col :span="8">
						<el-input v-model="patientName" placeholder="输入患者姓名…"></el-input>
					</el-col>

					<el-col :span="8">
						<el-button type="primary" icon="el-icon-search" @click="getMedicalInfos(1, MedicalPageSize)">搜索</el-button>
					</el-col>
				</el-row>
			</el-card>

			<el-card style="margin-bottom: 15px;">
				<div slot="header">
					<span class="el-icon-s-grid"></span> 医嘱记录
				</div>
				<div>
					<el-row v-if="MedicalTotalInfo > 0"  :gutter="15">
						<template v-for="(item, index) in MedicalInfos">
							
								<div class="register-panel">

									<div class="register-icon">
										<span class="el-icon-s-order"></span>
									</div>

									<div v-if="item.type==3">  
										<div class="register-title">
											<span class="register-doctor-name">药物类医嘱</span>
										</div>

										<div class="register-detail">
											<span class="register-detail-item">医嘱开具医师：{{ item.startDoctorName }}</span>
											<span class="register-detail-item">服药开始时间：{{ item.startTime }} </span>
											
										</div>
										
										<div class="Inhospital-change-icon">
											<el-button @click="getMedicineInfo(1, MedicinePageSize, index)" type="primary" size="small">查看详情</el-button>
										</div>
									</div>

									<div v-else>
										<div class="register-title">
											<span class="register-doctor-name">检验类医嘱</span>
										</div>

										<div class="register-detail">
											<span class="register-detail-item">医嘱开具医师：{{ item.startDoctorName }}</span>
											<span class="register-detail-item">检验单开具时间：{{ item.startTime }} </span>
											
										</div>
										
										<div class="Inhospital-change-icon">
											<el-button @click="getMedicineInfo3(1, MedicinePageSize, index)" type="primary" size="small">查看详情</el-button>
										</div>
									</div>
								</div>
						</template>
					</el-row>
					<el-empty v-else description="暂无相关记录"></el-empty>
					<el-pagination v-if="MedicalPageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange2"
						@current-change="handleCurrentChange2" :current-page="MedicalPageIndex" :page-sizes="[5, 10, 15, 30]"
						:page-size="MedicalPageSize" layout="total, sizes, prev, pager, next, jumper" :total="MedicalTotalInfo">
					</el-pagination>
				</div>
			</el-card>

				<el-dialog title="药物医嘱" width="1190px" :visible.sync="showMedicineFlag" :close-on-click-modal="false">
					<el-row>
						<el-descriptions class="margin-top" :column="2" :size="medium" border>
						<el-descriptions-item label="医嘱开具医师">{{ medicalAdvice.startDoctorName }}</el-descriptions-item>
						<el-descriptions-item label="医嘱号">{{ medicalAdvice.oid }}</el-descriptions-item>
						<el-descriptions-item label="医嘱内容">{{ medicalAdvice.content }}</el-descriptions-item>
						</el-descriptions>
					</el-row>
					
					<el-row>
						<el-card shadow="never" style="margin-top: 30px;">
							<div slot="header">医嘱药物列表</div>
							<div>
								<el-table v-loading="loading" stripe
									element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
									element-loading-background="rgba(124, 124, 124, 0.8)" :data="MedicinePageInfos" style="width: 100%" border>
										<el-table-column width="57" align="center" type="index" ></el-table-column>
										<el-table-column width="200" align="center" prop="medicineCommonName" label="药物名称"></el-table-column>
										<el-table-column width="200" align="center" prop="use" label="给药频率" :show-overflow-tooltip="true"></el-table-column>
										<el-table-column width="150" align="center" prop="medication" label="给药方式" :show-overflow-tooltip="true"></el-table-column>
										<el-table-column width="250" align="center" prop="startTime" label="给药起始时间" :show-overflow-tooltip="true"></el-table-column>
										<el-table-column width="250" align="center" prop="endTime" label="给药结束时间" :show-overflow-tooltip="true"></el-table-column>
								</el-table>
								<el-pagination v-if="MedicinePageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
									@current-change="handleCurrentChange" :current-page="MedicinePageIndex" :page-sizes="[8, 15, 30, 50]"
									:page-size="MedicinePageSize" layout="total, sizes, prev, pager, next, jumper" :total="MedicineTotalInfo">
								</el-pagination>
							</div>
						</el-card>
					</el-row>
			
					<div slot="footer" class="dialog-footer">
						<el-button @click="showMedicineFlag = false">关闭</el-button>
					</div>
				</el-dialog>

				<el-dialog title="检验医嘱" width="900px" :visible.sync="showInspectDetailflag">
					<el-row>
						<el-descriptions class="margin-top" :column="2" :size="medium" border>
						<el-descriptions-item label="医嘱开具医师">{{ medicalAdvice.startDoctorName }}</el-descriptions-item>
						<el-descriptions-item label="医嘱号">{{ medicalAdvice.oid }}</el-descriptions-item>
						<el-descriptions-item label="医嘱内容">{{ medicalAdvice.content }}</el-descriptions-item>
						</el-descriptions>
					</el-row>
					
					<el-row>
						<el-card shadow="never" style="margin-top: 30px;">
							<div slot="header">检验项目列表</div>
							<div>
								<el-table v-loading="loading" stripe
									element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
									element-loading-background="rgba(124, 124, 124, 0.8)" :data="MedicinePageInfos" style="width: 100%" border>
										<el-table-column width="57" align="center" type="index" ></el-table-column>
										<el-table-column width="150" align="center" prop="inspectionName" label="检验项目名称"></el-table-column>
										<el-table-column width="370" align="center" prop="inspectionContent" label="项目内容" :show-overflow-tooltip="true"></el-table-column>
										<el-table-column width="120" align="center" prop="inspectionTime" label="检验等待时间" :show-overflow-tooltip="true"></el-table-column>
										<el-table-column width="120" align="center" prop="inspectionPrice" label="检验价格" :show-overflow-tooltip="true"></el-table-column>
								</el-table>
								<el-pagination v-if="MedicinePageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
									@current-change="handleCurrentChange" :current-page="MedicinePageIndex" :page-sizes="[8, 15, 30, 50]"
									:page-size="MedicinePageSize" layout="total, sizes, prev, pager, next, jumper" :total="MedicineTotalInfo">
								</el-pagination>
							</div>
						</el-card>
					</el-row>					
				</el-dialog>
		</div>
        
		<el-dialog title="办理出院" width="700px" :visible.sync="showOutFlag">
			<el-form label-width="0px">
				<el-form-item v-if="patientMoney < 0">
				    <span style="font-family: 宋体;font-size: 10mm;color: red;">患者有未缴费用，请予以提醒！</span>
				</el-form-item>
				<el-form-item v-else>
				    <span style="font-family: 宋体;font-size: 10mm;color: royalblue;">患者费用已结清</span>
				</el-form-item>
		    </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showOutFlag = false" type="info">取 消</el-button>
				<el-button type="primary" v-if="flagg==1" @click="nextStep">下一步</el-button>
				<el-button type="primary" v-else @click="commitOut">办理出院确认</el-button>
			</div>
		</el-dialog>
		<el-dialog title="办理出院" width="800px" :visible.sync="showOutFlag2">
			<el-form label-width="0px">
				<el-form-item v-if="flagg==1">
				    <span style="font-family: 宋体;font-size: 10mm;color: red;">当前有正在进行的医嘱，是否继续强制出院</span>
				</el-form-item>
				<el-form-item v-else>
				    <span style="font-family: 宋体;font-size: 10mm;color: royalblue;">全部医嘱已执行完毕</span>
				</el-form-item>
		    </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showOutFlag2 = false" type="info">取 消</el-button>
				<el-button type="primary" @click="commitOut">办理出院确认</el-button>
			</div>
		</el-dialog>

		<el-dialog title="开具药物类医嘱" width="900px" :visible.sync="showAddFlag1">
			<el-form  label-width="140px" :model="medicalAdvice">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医嘱单号">
							<el-input v-model="medicalAdvice.oid" :disabled="true" auto-complete = "off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>

				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="患者姓名">
							<el-input v-model="medicalAdvice.patientName" :disabled="true" auto-complete = "off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="住院科室">
							<el-input v-model="medicalAdvice.departmentName" :disabled="true"></el-input>
						</el-form-item>     
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="15">
						<el-form-item label="医嘱内容">
							<el-input v-model="medicalAdvice.content" auto-complete = "off"
							type="textarea"
							resize="none"
							:autosize="{ minRows: 4, maxRows: 4 }"
							placeholder="请输入内容">
							</el-input>
						</el-form-item>
					</el-col>
				</el-row>
				
				
				<div  v-for="(medicineform, index) in medicalAdvice.medicine_forms" :key="medicineform.key">
					<el-row :gutter="65">
						<el-col :span="1" :offset="2">
							<el-button type="text" size="medium">药物{{(index+1)}}</el-button>
						</el-col>
						<el-col :span="1" >
							<el-button circle class="el-icon-delete" type="danger" size="mini" @click.prevent="removeDomain(medicineform)"></el-button>
						</el-col>
						<el-col :span="1">
							<el-button circle class="el-icon-plus" size="mini" type="primary" @click.prevent="addmedicineform"></el-button>
						</el-col>
					</el-row>

					<el-row :gutter="15">
						<el-col :span="12">
							<el-form-item label="药品通用名">
								<el-input v-model="medicineform.common_name" auto-complete = "off"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="12">
							<el-form-item label="给药方式">
								<el-select v-model="medicineform.medication" placeholder="给药方式">
									<el-option label="口服" value="口服"></el-option>
									<el-option label="注射" value="注射"></el-option>
									<el-option label="涂抹" value="涂抹"></el-option>
									<el-option label="含化" value="含化"></el-option>
									<el-option label="填塞" value="填塞"></el-option>
									<el-option label="灌肠" value="灌肠"></el-option>
									<el-option label="灌注" value="灌注"></el-option>
									<el-option label="雾化" value="雾化"></el-option>
								</el-select>
							</el-form-item>
						</el-col>
					</el-row>
					
					<el-row>
						<el-col :span="12">

							<el-form-item label="开始时间">
								<el-date-picker
								class="datestyle"
								v-model="medicineform.start_time"
								type="date"
								clearable
								placeholder="开始时间"
								value-format="yyyy-MM-dd"></el-date-picker>
							</el-form-item>
							
						</el-col>
						<el-col :span="12">
							<el-form-item label="结束时间">
								<el-date-picker
								class="datestyle"
								v-model="medicineform.end_time"
								type="date"
								clearable
								placeholder="结束时间"
								value-format="yyyy-MM-dd"></el-date-picker>
							</el-form-item>
						</el-col>
					</el-row>

					<el-row>
						<el-col :span="8">
							<el-form-item label="用药周期">
								<el-input v-model="medicineform.freq" auto-complete = "off" placeholder="天"></el-input>
							</el-form-item>
						</el-col>
					</el-row>

					<el-row>
						<el-col :span="8">
							<el-form-item label="每个周期用药次数">
								<el-input v-model="medicineform.times" auto-complete = "off" placeholder="次/天"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					
					<el-row>
						<el-col :span="8">
							<el-form-item label="每次用药剂量">
								<el-input v-model="medicineform.dose" auto-complete = "off" placeholder="单位/次"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					
				</div>

				<el-form-item>
					<el-button type="primary" @click="addmedicineform">增加药品</el-button>
					<el-button type="primary" @click="submitMedicalAdvice(medicalAdvice)">提交医嘱</el-button>
				</el-form-item>
			</el-form>
			
		</el-dialog>


		<el-dialog title="开具检验类医嘱" width="700px" :visible.sync="showAddFlag2">
			
			<el-form  label-width="110px" :model="medicalAdvice">

				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="医嘱单号">
							<el-input v-model="medicalAdvice.oid" :disabled="true" auto-complete = "off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>

				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="患者姓名">
							<el-input v-model="medicalAdvice.patientName" :disabled="true" auto-complete = "off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="住院科室">
							<el-input v-model="medicalAdvice.departmentName" :disabled="true"></el-input>
						</el-form-item>     
					</el-col>
				</el-row>

				<el-row :gutter="15">
					<el-col :span="18">
						<el-form-item label="医嘱内容">
							<el-input v-model="medicalAdvice.content" auto-complete = "off"
							type="textarea"
							resize="none"
							:autosize="{ minRows: 4, maxRows: 4 }"
							placeholder="请输入内容">
							</el-input>
						</el-form-item>
					</el-col>
				</el-row>

				<div  v-for="(medicineform, index) in medicalAdvice.medicine_forms" :key="medicineform.key">
					<el-row :gutter="65">
						<el-col :span="1" :offset="2">
							<el-button type="text" size="medium">项目{{(index+1)}}</el-button>
						</el-col>
						<el-col :span="1" >
							<el-button circle class="el-icon-delete" type="danger" size="mini" @click.prevent="removeDomain(medicineform)"></el-button>
						</el-col>
						<el-col :span="1">
							<el-button circle class="el-icon-plus" size="mini" type="primary" @click.prevent="addmedicineform"></el-button>
						</el-col>
					</el-row>

					<el-row :gutter="15">
						<el-col :span="12">
							<el-form-item label="检验项目名">
								<el-input v-model="medicineform.inspectionName" auto-complete = "off"></el-input>
							</el-form-item>

						</el-col>
						<el-col :span="12">
							<el-form-item label="检验时间">
								<el-date-picker
								class="datestyle"
								v-model="medicineform.start_time"
								type="date"
								clearable
								placeholder="检验时间"
								value-format="yyyy-MM-dd"></el-date-picker>
							</el-form-item>

						</el-col>
					</el-row>
				</div>
				
				<el-form-item>
					<el-button type="primary" @click="addmedicineform">增加检验项目</el-button>
					<el-button type="primary" @click="submitMedicalAdvice(medicalAdvice)">提交医嘱</el-button>
					<el-button type="primary" @click="showAddFlag2=false">取消</el-button>
				</el-form-item>

			</el-form>

			

		</el-dialog>
		
		
        
    </div>
</template>

<script>
import { 
	getLoginUser,
	getPageUserHospitalization,
	upMedicalAdvice,
	upOuthospital,
	getPageMedicalInfos,
	getMoneyInfo,
} from '../api/index.js';

export default {
    data(){

        return {
			showOutFlag: false,
			showOutFlag2: false,

			pageInfos: [],
			pageIndex: 1,
			pageSize: 10,
			pageTotal: 0,
			totalInfo: 0,
			loading: true,

			showAddFlag1: false,
			showAddFlag2: false,

            showdetailflag: false,

			qryForm: {
				patientName: "",
				phone: "",
				address: "",
				gender: "",
				status: "",
			},

			medicalAdvice: {
				doctorId: '',
				inhospital_log: '',
				type: '',
				oid: '',
				content: '',
				medicine_forms: [{
					inspectionName: '',
					start_time: '',
					end_time: '',
					common_name: '',
					madication: '',
					freq: '',
					dose: '',
					times: '',
					}
				],
			},

			initMA: {
				doctorId: '',
				inhospital_log: '',
				type: '',
				oid: '',
				content: '',
				medicine_forms: [{
					inspectionName: '',
					start_time: '',
					end_time: '',
					common_name: '',
					madication: '',
					freq: '',
					dose: '',
					times: '',
					}
				],
			},


			resForm: {
				nowDate: "",
				setNowDate: "",
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


			MedicalInfos: [],
			MedicalPageIndex: 1,
			MedicalPageSize: 5,
			MedicalPageTotal: 0,
			MedicalTotalInfo: 0,


			MedicinePageInfos: [],
			MedicinePageIndex: 1,
			MedicinePageSize: 10,
			MedicinePageTotal: 0,
			MedicineTotalInfo: 0,
			patientMoney: 0,

			patientName: "",
			type: '',
			showMedicineFlag: false,
			oid: '',
			index: 0,
			flagg: 0,


			shownoticeflag: false,

			inspectionForm:{},
			showInspectDetailflag: false,
			
			outForm: {
				inHospitalLog: 0,
				flag: 1,
			},
        }
    },
    methods: {

		getMedicineInfo(pageIndex, pageSize, index) {
			this.medicalAdvice = this.MedicalInfos[index];
			this.oid = this.medicalAdvice.oid;
			
			this.loading = true;
			this.index = index;
			this.type = 5;
			getPageMedicalInfos(pageIndex, pageSize, this.$store.state.token, this.patientName, this.oid, this.type).then(resp => {
					
					this.MedicinePageInfos = resp.data.data;
					this.MedicinePageIndex = resp.data.pageIndex;
					this.MedicinePageSize =  resp.data.pageSize;
					this.MedicinePageTotal = resp.data.pageTotal;
					this.MedicineTotalInfo = resp.data.count;
					this.showMedicineFlag = true;
				});
			this.loading = false;
			
		},
		getMedicineInfo2(pageIndex, pageSize) {
			this.loading = true;
			this.type = 2;
			getPageMedicalInfos(pageIndex, pageSize, this.$store.state.token, this.patientName, this.oid, this.type).then(resp => {
					
					this.MedicinePageInfos = resp.data.data;
					this.MedicinePageIndex = resp.data.pageIndex;
					this.MedicinePageSize =  resp.data.pageSize;
					this.MedicinePageTotal = resp.data.pageTotal;
					this.MedicineTotalInfo = resp.data.count;
				});
			this.loading = false;
		},
		getMedicineInfo3(pageIndex, pageSize, index) {
			this.medicalAdvice = this.MedicalInfos[index];
			this.oid = this.medicalAdvice.oid;
			
			this.loading = true;
			this.index = index;
			this.type = 5;
			getPageMedicalInfos(pageIndex, pageSize, this.$store.state.token, this.patientName, this.oid, this.type).then(resp => {
					this.MedicinePageInfos = resp.data.data;
					this.MedicinePageIndex = resp.data.pageIndex;
					this.MedicinePageSize =  resp.data.pageSize;
					this.MedicinePageTotal = resp.data.pageTotal;
					this.MedicineTotalInfo = resp.data.count;
					this.showInspectDetailflag = true;
					});

			this.loading = false;
			
		},
		
		
		getPageInfo(pageIndex, pageSize) {
		
			getPageUserHospitalization(pageIndex, pageSize, this.$store.state.token, this.qryForm.name, 
								this.qryForm.phone, this.qryForm.address, this.qryForm.status, this.qryForm.gender).then(resp => {

				this.pageInfos = resp.data.data;
				this.pageIndex = resp.data.pageIndex;
				this.pageSize = resp.data.pageSize;
				this.pageTotal = resp.data.pageTotal;
				this.totalInfo = resp.data.count;
			});
			this.loading = false;
		},


		handleSizeChange(pageSize){
		
			this.getMedicineInfo2(1, pageSize);
		},
		handleCurrentChange(pageIndex){
		
			this.getMedicineInfo2(pageIndex, this.MedicinePageSize);
		},
		handleSizeChange2(pageSize){
		
			this.getDeal(1, pageSize);
		},
		handleCurrentChange2(pageIndex){
		
			this.getDeal(pageIndex, this.dealPageSize);
		},
		handleSizeChange3(pageSize){
		
			this.getMedicineInfo2(1, pageSize);
		},
		handleCurrentChange3(pageIndex){
		
			this.getMedicineInfo2(pageIndex, this.MedicinePageSize);
		},
		handleSizeChange4(pageSize){
		
			this.getMedicalInfos(1, pageSize);
		},
		handleCurrentChange4(pageIndex){
		
			this.getMedicalInfos(pageIndex, this.MedicalPageSize);
		},
		handleSizeChange2(pageSize){
		
			this.getMedicalInfos(1, pageSize);
		},
		handleCurrentChange2(pageIndex){ 
			this.getMedicalInfos(pageIndex, this.MedicalPageSize);
		},

		addMedcalAdvice(index,advicetype){
			this.medicalAdvice = JSON.parse(JSON.stringify(this.initMA))

			this.medicalAdvice.inhospital_log = this.pageInfos[index].id;
			this.medicalAdvice.patientName = this.pageInfos[index].patientName;
			this.medicalAdvice.departmentName = this.pageInfos[index].departmentName;
			

			//生成随机的医嘱流水号
			let yy = new Date().getFullYear();
			let mm = new Date().getMonth()+1;
			let dd = new Date().getDate();
			let hh = new Date().getHours();
			let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
			let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();

			this.medicalAdvice.oid = '10'+this.medicalAdvice.inhospital_log+yy+mm+dd+hh+mf+ss;


			if(advicetype==1){
				this.medicalAdvice.type = '3'; //药物类医嘱
				this.showAddFlag1 = true;
				
			}
			else{
				this.medicalAdvice.type = '4'; //检验类医嘱
				this.showAddFlag2 = true;
				
			}
		},


		//	药物医嘱的添加删除
		removeDomain(item) {
			var index = this.medicalAdvice.medicine_forms.indexOf(item)
			if (index !== -1) {
			this.medicalAdvice.medicine_forms.splice(index, 1)
			}
		},

		addmedicineform(){
			 this.medicalAdvice.medicine_forms.push({
          		value: '',
          		key: Date.now()
        	});
		},
		
		nextStep(){
			this.showOutFlag = false;
			this.showOutFlag2 = true;
		},
		
		//提交医嘱
		submitMedicalAdvice(medicalAdvice){
			medicalAdvice.doctorId = this.loginUser.id;
			
			

			upMedicalAdvice(medicalAdvice).then(resp =>{
				this.$message({
					message: '开具医嘱成功:)',
					type: 'success'
				});
			this.medicalAdvice = JSON.parse(JSON.stringify(this.initMA))
			this.showAddFlag1 = false;
			this.showAddFlag2 = false;
			});
		},


		//获取患者的历史医嘱
		getMedicalInfos(pageIndex, pageSize) {
			this.oid = '';
			this.type = 4;
			getPageMedicalInfos(pageIndex, pageSize, this.$store.state.token, this.patientName, this.oid, this.type).then(resp => {
				
				this.MedicalInfos = resp.data.data;
				this.MedicalPageIndex = resp.data.pageIndex;
				this.MedicalPageSize =  resp.data.pageSize;
				this.MedicalPageTotal = resp.data.pageTotal;
				this.MedicalTotalInfo = resp.data.count;
			});
		},
		
		outhospital(id){
			this.outForm.inHospitalLog = id;
			getMoneyInfo(this.$store.state.token, id).then(resp =>{
				this.patientMoney = resp.data;
			});
			getPageMedicalInfos(1, 10000, this.$store.state.token, '', '', 3).then(resp =>{
				this.flagg = resp.data.flag;
			});
			if (this.patientMoney < 0){
				this.showOutFlag = true;
			} else if (this.flagg == 1){
				this.showOutFlag2 = true;
			} else {
				this.showOutFlag = true;
			}
		},
		
		commitOut(){
			upOuthospital(this.outForm).then(resp =>{
				if (resp.code == 0){
					this.$message({
					    message: '提交成功！',
					    type: 'success'
					});
				} else {
					this.$message({
					    message: '提交失败！',
					    type: 'error'
					});
				}
				
				this.showOutFlag = false;
				this.showOutFlag2 = false;
				location.reload();
			});
		},

		filterHandler(value, row, column) {
			const property = column['property'];
			return row[property] === value;
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
