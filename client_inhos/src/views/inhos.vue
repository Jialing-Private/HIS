<template>
    <div>
		<div class="mybody">
			<el-image class="inhos-img" :src="require('@/assets/doctor-pink.svg')"></el-image>

			<div class = "inhos-user-info">
				<el-row v-if="inhosTotalInfo > 0"  :gutter="15">
					<el-descriptions style="background-color: #FFFFFF; padding: 15px;" title="住院档案" :column="1" border>
						<template slot="extra">
							<el-button @click="showUpdBedsWin()" type="primary" size="small">修改</el-button>
						</template>
					    <el-descriptions-item label="用户姓名">{{ inhosPageInfos[0].patientName }} </el-descriptions-item>
					    <el-descriptions-item label="住院科室">{{ inhosPageInfos[0].doctorDepartmentName }}</el-descriptions-item>
					    <el-descriptions-item label="主治医师">{{ inhosPageInfos[0].doctorName }}</el-descriptions-item>
					    <el-descriptions-item label="入院时间">{{ inhosPageInfos[0].hospitalizationStartTime }}</el-descriptions-item>
					    <el-descriptions-item label="住院床位">{{ inhosPageInfos[0].bedBid }}</el-descriptions-item>
					    <el-descriptions-item label="可用余额">{{ patientMoney }}元</el-descriptions-item>
					</el-descriptions>
					<el-dialog title="电子住院单" width="700px" :visible.sync="showBedFormflag">
						<el-form label-width="110px" :model="hospitalizationForm">
							<el-row :gutter="15">
					            <el-col :span="12">
					                <el-form-item label="患者姓名">
					                    <el-input v-model="inhosPageInfos[0].patientName" :disabled="true" auto-complete = "off"></el-input>
					                </el-form-item>
					            </el-col>
					            <el-col :span="12">
					                <el-form-item label="住院科室">
					                    <el-input v-model="inhosPageInfos[0].departmentName" :disabled="true"></el-input>
					                </el-form-item>     
					            </el-col>
					        </el-row>
					
							<el-row :gutter="15">
					            <el-col :span="12">
					                <el-form-item label="主治医师">
					                    <el-input v-model="inhosPageInfos[0].doctorName" :disabled="true" auto-complete = "true"></el-input>
					                </el-form-item>
					            </el-col>
					            <el-col :span="12">
					                <el-form-item label="住院单开具时间">
					                    <el-input v-model="inhosPageInfos[0].createTime" :disabled="true" auto-complete = "true"></el-input>
					                </el-form-item>     
					            </el-col>
					        </el-row>
					
							<el-row :gutter="15">
								<el-form-item label="选择入院时间">
									<el-date-picker
									class="datestyle"
									v-model="inhosPageInfos[0].hospitalizationStartTime"
									type="date"
									clearable
									placeholder="入院时间"
									value-format="yyyy-MM-dd" :disabled="true">
									</el-date-picker>
								</el-form-item>
							</el-row>	
					
							<el-row :gutter="15">
								<el-form-item label="选择住院床位">
									<el-select style="width:100%;" v-model="inhosPageInfos[0].bedId" placeholder="请选择床位">
										<el-option label="查看全部" value=""></el-option>
										<el-option v-for="(item, index) in this.availableBeds" 
											:key="index" :label="item.info" :value="item.id"></el-option>
									</el-select>
								</el-form-item>
							</el-row>
							<el-form-item size="mini">
								<el-button type="primary" @click="completeInhospital(inhosPageInfos[0])">提交申请</el-button>
							 	<el-button @click="showBedFormflag = false">取消</el-button>
							</el-form-item>
						</el-form>
					</el-dialog>
				</el-row>
				<el-row v-else>
					<el-descriptions style="background-color: #FFFFFF; padding: 15px;" title="住院档案" :column="1" border>
					<el-descriptions-item label="用户姓名">{{ loginUser['name'] }} </el-descriptions-item>
					<el-descriptions-item label="住院科室">暂无相关记录</el-descriptions-item>
					<el-descriptions-item label="主治医师">暂无相关记录</el-descriptions-item>
					<el-descriptions-item label="入院时间">暂无相关记录</el-descriptions-item>
					<el-descriptions-item label="住院床位">暂无相关记录</el-descriptions-item>
					<el-descriptions-item label="可用余额">{{ patientMoney }}元</el-descriptions-item>
					</el-descriptions>
				</el-row>
			</div>

			

			<div class="inhos-steps">
				<el-card style="margin-bottom: 15px;">
				<div slot="header">
					<span class="el-icon-s-grid"></span>  入院流程
				</div>
				<div style="height: 280px;">
					<el-steps direction="vertical" :active="this.active" finish-status="success">
						<el-step title="入院通知" description="由门诊医师开具电子住院通知单"></el-step>
						<el-step title="入院登记" description="登记入院时间、选择床位"></el-step>
						<el-step title="电子钱包充值" description="缴纳预交金，方便后续自动扣费等业务"></el-step>
					</el-steps>
				</div>
				</el-card>
			</div>
			
			
			<div class="inhos-cards" >
				<el-card style="margin-bottom: 15px;">
					<div slot="header">
						<span class="el-icon-s-grid"></span> 入院/出院通知
					</div>
					<div>
					<el-row v-if="inhosTotalInfo > 0">
						<el-row v-if="inhosPageInfos[0].status == '待出院'" :gutter="15">
							<el-col :span="8">
								<div class="register-panel">
									<div class="register-icon">
										<span class="el-icon-s-order"></span>
									</div>
							
									<div class="register-title">
										<span class="register-doctor-name">电子出院单</span>
									</div>
							
									<div class="register-detail">
										<span class="register-detail-item">主治医师：{{ inhosPageInfos[0].doctorName }}</span>
										<span class="register-detail-item">开单日期：{{ inhosPageInfos[0].updateTime }} </span>
									</div>
							
									<div class="Inhospital-change-icon">
										<el-button @click="showOuthosDetailflag = true" type="primary" size="small">查看</el-button>
									</div>
							
	
								</div>
							</el-col>
							<el-dialog title="电子住院单" width="700px" :visible.sync="showOuthosDetailflag">
								<el-form label-width="110px" :model="hospitalizationForm">
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="患者姓名">
							                    <el-input v-model="inhosPageInfos[0].patientName" :disabled="true" auto-complete = "off"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院科室">
							                    <el-input v-model="inhosPageInfos[0].departmentName" :disabled="true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="主治医师">
							                    <el-input v-model="inhosPageInfos[0].doctorName" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院单开具时间">
							                    <el-input v-model="inhosPageInfos[0].createTime" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
										<el-col :span="12">
										<el-form-item label="入院时间">
											<el-date-picker
											class="datestyle"
											v-model="inhosPageInfos[0].hospitalizationStartTime"
											type="date"
											clearable
											placeholder="入院时间"
											:disabled="true"
											:picker-options="DisableDatesOption"
											value-format="yyyy-MM-dd">
											</el-date-picker>
										</el-form-item>
										</el-col>
										<el-col :span="12">
										<el-form-item label="住院床位">
											<el-select style="width:100%;" v-model="inhosPageInfos[0].bedId" :disabled="true" placeholder="请选择床位">
												<el-option label="查看全部" value=""></el-option>
												<el-option v-for="(item, index) in this.availableBeds" 
													:key="index" :label="item.info" :value="item.id"></el-option>
											</el-select>
										</el-form-item>
										</el-col>
									</el-row>	
							
									<el-row :gutter="15">
										
									</el-row>
									<el-form-item size="mini">
										<el-button type="primary" @click="outhospital(inhosPageInfos[0].id, 2)">确认出院</el-button>
									 	<el-button @click="showOuthosDetailflag = false">取消</el-button>
									</el-form-item>
								</el-form>
							</el-dialog>
							</el-row>
						<el-row v-else-if="inhosPageInfos[0].status == '待入院'"  :gutter="15">
							<el-col :span="8">
								<div class="register-panel">
									<div class="register-icon">
										<span class="el-icon-s-order"></span>
									</div>
							
									<div class="register-title">
										<span class="register-doctor-name">电子住院单</span>
									</div>
							
									<div class="register-detail">
										<span class="register-detail-item">主治医师：{{ inhosPageInfos[0].doctorName }}</span>
										<span class="register-detail-item">开单日期：{{ inhosPageInfos[0].createTime }} </span>
									</div>
							
									<div class="Inhospital-change-icon" v-if="inhosPageInfos[0].status=='待入院'">
										<el-button @click="getDepartmentId" type="primary" size="small">入院登记</el-button>
									</div>
							
									<div class="Inhospital-yes-icon" v-if="inhosPageInfos[0].status=='待入院'">
										<el-button @click="refuseFlag=true" type="danger" size="small">撤销入院</el-button>
									</div>
							
								</div>
							</el-col>
							<el-dialog title="电子住院单" width="700px" :visible.sync="showInhosDetailflag">
								<el-form label-width="110px" :model="hospitalizationForm">
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="患者姓名">
							                    <el-input v-model="inhosPageInfos[0].patientName" :disabled="true" auto-complete = "off"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院科室">
							                    <el-input v-model="inhosPageInfos[0].departmentName" :disabled="true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="主治医师">
							                    <el-input v-model="inhosPageInfos[0].doctorName" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院单开具时间">
							                    <el-input v-model="inhosPageInfos[0].createTime" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
										<el-form-item label="选择入院时间">
											<el-date-picker
											class="datestyle"
											v-model="inhosPageInfos[0].hospitalizationStartTime"
											type="date"
											clearable
											placeholder="入院时间"
											:picker-options="DisableDatesOption"
											value-format="yyyy-MM-dd">
											</el-date-picker>
										</el-form-item>
									</el-row>	
							
									<el-row :gutter="15">
										<el-form-item label="选择住院床位">
											<el-select clearable style="width:100%;" v-model="inhosPageInfos[0].bedId" placeholder="请选择床位">
												<el-option label="查看全部" value=""></el-option>
												<el-option v-for="(item, index) in this.availableBeds" 
													:key="index" :label="item.info" :value="item.id"></el-option>
											</el-select>
										</el-form-item>
									</el-row>
									<el-form-item size="mini">
										<el-button type="primary" @click="completeInhospital(inhosPageInfos[0])">确认入院</el-button>
									 	<el-button @click="showInhosDetailflag = false">取消</el-button>
									</el-form-item>
								</el-form>
							</el-dialog>
							<el-dialog title="拒绝入院确认" width="700px" :visible.sync="refuseFlag">
								<el-form label-width="0px">
									<el-row :gutter = "15">
										<el-form-item>
											请输入自己的姓名并确认：
										</el-form-item>
									</el-row>
									<el-form-item>
										<el-input v-model="refusechar" placeholder="" autocomplete="off"></el-input>
									</el-form-item>
								</el-form>
									
								<div slot="footer" class="dialog-footer">
									<el-button type="danger" @click="refuseInhospital(inhosPageInfos[0])">确认</el-button>
									<el-button @click="refuseFlag=false">取消</el-button>
								</div>
							</el-dialog>
						</el-row>
						<el-row v-else-if="inhosPageInfos[0].status == '已入院'"  :gutter="15">
							<el-col :span="8">
								<div class="register-panel">
									<div class="register-icon">
										<span class="el-icon-s-order"></span>
									</div>
							
									<div class="register-title">
										<span class="register-doctor-name">电子住院单</span>
									</div>
							
									<div class="register-detail">
										<span class="register-detail-item">主治医师：{{ inhosPageInfos[0].doctorName }}</span>
										<span class="register-detail-item">开单日期：{{ inhosPageInfos[0].createTime }} </span>
									</div>
							
									<div class="Inhospital-change-icon" v-if="inhosPageInfos[0].status=='已入院'">
										<el-button @click="showInhosDetailflag2 = true" type="primary" size="small">查看</el-button>
									</div>
							
								</div>
							</el-col>
							<el-dialog title="电子住院单" width="700px" :visible.sync="showInhosDetailflag2">
								<el-form label-width="110px" :model="hospitalizationForm">
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="患者姓名">
							                    <el-input v-model="inhosPageInfos[0].patientName" :disabled="true" auto-complete = "off"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院科室">
							                    <el-input v-model="inhosPageInfos[0].departmentName" :disabled="true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
							            <el-col :span="12">
							                <el-form-item label="主治医师">
							                    <el-input v-model="inhosPageInfos[0].doctorName" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>
							            </el-col>
							            <el-col :span="12">
							                <el-form-item label="住院单开具时间">
							                    <el-input v-model="inhosPageInfos[0].createTime" :disabled="true" auto-complete = "true"></el-input>
							                </el-form-item>     
							            </el-col>
							        </el-row>
							
									<el-row :gutter="15">
										<el-col :span="12">
										<el-form-item label="入院时间">
											<el-date-picker
											class="datestyle"
											v-model="inhosPageInfos[0].hospitalizationStartTime"
											type="date"
											:disabled="true"
											placeholder="入院时间"
											:picker-options="DisableDatesOption"
											value-format="yyyy-MM-dd">
											</el-date-picker>
										</el-form-item>
										</el-col>
										<el-col :span="12">
											<el-form-item label="住院床位">
												<el-input v-model="inhosPageInfos[0].bedBid" :disabled="true" auto-complete = "true"></el-input>
												</el-select>
											</el-form-item>
										</el-col>
									</el-row>
									
									<el-row :gutter="15">
										<el-col :span="12">
										<el-form-item label="出院时间">
											<el-date-picker
											class="datestyle"
											v-model="inhosPageInfos[0].hospitalizationEndTime"
											type="date"
											:disabled="true"
											placeholder="暂无"
											value-format="yyyy-MM-dd">
											</el-date-picker>
										</el-form-item>
										</el-col>
									</el-row>
									<el-form-item size="mini">
									 	<el-button @click="showInhosDetailflag2 = false">关闭</el-button>
									</el-form-item>
								</el-form>
							</el-dialog>
						</el-row>
					</el-row>
					<el-empty v-else description="暂无相关记录"></el-empty>
					</div>
				</el-card>


				<el-card style="margin-bottom: 15px;">
					<div slot="header">
						<span class="el-icon-s-grid"></span> 电子钱包
					</div>

					<div>
						<el-row :gutter="15">
							<div class = "register-panel">
								<div class="register-icon">
									<span class="el-icon-bank-card"></span>
								</div>
								
								<div class="money-title">
									<span>可用余额：</span>
								</div>

								<div class="money-number">
									<span class="number">{{ patientMoney }}<span style="font-size: 7mm;color:grey">元</span></span>
								</div>

								<div class="Inhospital-change-icon">
									<el-button @click="addmoneyflag = true" type="primary" size="small">钱包充值</el-button>
								</div>

								<div class="Inhospital-pull">
									<el-button @click="getDeal(1, dealPageSize)" type="info" size="small">查看明细</el-button>
								</div>

								<div class="Inhospital-yes-icon" >
									<el-button @click="minusmoneyflag = true" type="primary" size="small">零钱提现</el-button>
								</div>
							</div>
						</el-row>
					</div>

				</el-card>

				<el-card style="margin-bottom: 15px;" v-show="MedicalPageTotal > 0">
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
												<span class="register-detail-item">医嘱开具时间：{{ item.createTime }} </span>
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
						<el-pagination v-if="MedicalPageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange4"
							@current-change="handleCurrentChange4" :current-page="MedicalPageIndex" :page-sizes="[5, 10, 15, 30]"
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
			
			<el-dialog title="钱包充值" width="400px" :visible.sync="addmoneyflag">
				<el-form label-width="110px" :model="newForm">
					<el-row :gutter = "15">
						<el-form-item label="充值金额">
							<el-input v-model="newForm.addmoneynum" placeholder="请输入充值金额…" autocomplete="off"></el-input>
						</el-form-item>  
					</el-row>
					<el-row :gutter="15">
						<el-form-item label="选择支付方式" placeholder="请选择支付方式">
							<el-select v-model="newForm.paymethod" >
								<el-option label="支付宝" value="支付宝"></el-option>
								<el-option label="微信支付" value="微信"></el-option>
								<el-option label="VISA" value="VISA"></el-option>
							</el-select>
						</el-form-item>
					</el-row>
				</el-form>
					
				<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="completeAddmoney">确认充值</el-button>
					<el-button @click="addmoneyflag = false">取消</el-button>
				</div>
			</el-dialog>

			<el-dialog title="提现" width="400px" :visible.sync="minusmoneyflag">
				<el-form label-width="110px" :model="newForm">
					<el-row :gutter = "15">
						<el-form-item label="提现金额">
							<el-input v-model="newForm.minusmoneynum" placeholder="请输入提现金额…" autocomplete="off"></el-input>
						</el-form-item>  
					</el-row>
					<el-row :gutter="15">
						<el-form-item label="选择提现方式" placeholder="请选择提现方式">
							<el-select v-model="newForm.paymethod" >
								<el-option label="支付宝" value="支付宝"></el-option>
								<el-option label="微信支付" value="微信"></el-option>
								<el-option label="VISA" value="VISA"></el-option>
							</el-select>
						</el-form-item>
					</el-row>
				</el-form>
					
				<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="completeMinusmoney">确认提现</el-button>
					<el-button @click="minusmoneyflag = false">取消</el-button>
				</div>
			</el-dialog>
			
			<el-dialog title="交易记录" width="1300px" :visible.sync="showDealFlag" :close-on-click-modal="false">
				<el-card>
				<div slot="header" class="dialog-header">
					<el-button type="success" size="mini" icon="el-icon-download"
							@click="exportData">导出</el-button>
				</div>
				<div>
				<el-table v-loading="loading" stripe
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="dealPageInfos" border>
						<el-table-column align="center" type="index" ></el-table-column>
						<el-table-column align="center" prop="id" label="交易编号"></el-table-column>
						<el-table-column align="center" prop="dealTime" label="交易时间"></el-table-column>
						<el-table-column align="center" prop="price" label="交易金额" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="paymethod" label="交易方式" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="type" label="交易类型" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="inHospitalDepartmentName" label="住院部门" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="medicalAdviceOid" label="医嘱单号" :show-overflow-tooltip="true"></el-table-column>
						<el-table-column align="center" prop="bedPrice" label="床位价格"></el-table-column>
				</el-table>
				</div>

				<el-pagination v-if="dealPageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange2"
					@current-change="handleCurrentChange2" :current-page="dealPageIndex" :page-sizes="[8, 16, 25, 50]"
					:page-size="dealPageSize" layout="total, sizes, prev, pager, next, jumper" :total="dealTotalInfo">
				</el-pagination>
				</el-card>
				<div slot="footer" class="dialog-footer">
					<el-button @click="showDealFlag = false">关闭</el-button>
				</div>
			</el-dialog>


			<el-dialog title="出院提示" width="600px" :visible.sync="moneyOutFlag">
				<span>您的钱包余额尚有未支付的款项，请支付后进行出院操作！</span>
				<div slot="footer" class="dialog-footer">
					<el-button @click="moneyOutFlag = false" type="primary">确定</el-button>
				</div>
			</el-dialog>

			<el-dialog title="出院提示" width="600px" :visible.sync="moneyOutFlag2">
				<span>您的钱包余额{{this.patientMoney}}元，尚未全部提现，确认出院后将自动退回原支付方。是否确认出院？</span>
				<div slot="footer" class="dialog-footer">
					<el-button @click="moneyOutFlag2 = false" type="info">取 消</el-button>
					<el-button type="primary" @click="commitOut">确认出院</el-button>
				</div>
			</el-dialog>
			
		</div>


    </div>
        
      
    
</template>

<style>
</style>

<script>
import {
  getPageUserHospitalization,
  upcompleteInhospital,
  getAvailableBedsInfo,
  getMoneyInfo,
  upaddpatientmoney,
  getPageMedicalInfos,
  getLoginUser,
  upminuspatientmoney,
  exportDealInfo,
  getDealInfo,
  upOuthospital,
} from "../api";
import { mapState } from "vuex";
export default {

    data() {
		
        let _this = this;
        return {
			showInspectDetailflag: false,
			maflag: 0,


			loading: true,
            active: 0,
			loginUser: {},
			showOuthosDetailflag: false,
			showMedicineFlag: false,
			showBedFormflag: false,
			originalBedId: 0,
			availableBeds: [],
            inhosPageInfos: [],
			inhosPageIndex: 1,
			inhosPageSize: 12,
			inhosPageTotal: 0,
			inhosTotalInfo: 0,
			MedicalInfos: [],
			MedicalPageIndex: 1,
			MedicalPageSize: 5,
			MedicalPageTotal: 0,
			MedicalTotalInfo: 0,
            showUpdUserFlag: false,
			MedicinePageInfos: [],
			MedicinePageIndex: 1,
			MedicinePageSize: 8,
			MedicinePageTotal: 0,
			MedicineTotalInfo: 0,
			refusechar: '',
			refuseFlag: false,
			patientName: '',
            
            showInhosDetailflag: false,
			showInhosDetailflag2: false,

			patientMoney: 0,
            addmoneynum: 0,
            addmoneyflag: false,
            moneyDetailfalg: false,
			oid: '',
			index: 0,
			type: '',

            hospitalizationForm: {
				id: "",
				patientId: '',
				patientName: '',
				createTime: '',

				hospitalizationStartTime: '',
				hospitalizationEndTime: '',

				status: '',
				bedId: '',
				bedBid:'',
				departmentId: '',
				departmentName:'',
				doctorName:''
			},
			
			bedForm: {
				id: "",
				patientId: "",
				patientName: "",
				hospitalizationStartTime: "",
				hospitalizationEndTime: "",
				status: "",
				bedId: "",
				departmentId: "",
				departmentName: "",
				doctorName: "",
				doctorId: "",
			},

			medicalAdvice:{
				oid: '',
				content:'',
				type: '',
				
				startDoctorId: '',
				startDoctorName: '',
				startTime: '',
				endTime: '',
				endDoctorName: '',
				endDoctorId: '',

				medicineCommonName: '',
				dose: 0,
				times: 0,
				allFreq: 0,
				
				medicineUnit: '',
				freq: '',
				
				price: '',
				
				inspectionName: '',
				inspectPreTime:'',
				inspectTime: '',			
			},
			resForm: {
				nowDate: "",
				setNowDate: "",
			},
			newForm: {
				addmoneynum: 0,
				paymethod: "",
				token: "",
			},
			DisableDatesOption: {
				disabledDate(time) {
					_this.resForm.setNowDate = _this.resForm.nowDate;
					let curDate = (new Date()).getTime();
					let pre = new Date();
					let thirtyonedays = 31 * 24 * 3600 * 1000;
					let oneday = curDate - 24 * 3600 * 1000;
					let oneMonth = curDate + thirtyonedays;
					return time.getTime() < oneday || time.getTime() > oneMonth;
				}
			},
			
			inspectionForm:{},
			minusmoneyflag: false,
			showDealFlag: false,
			dealPageInfos: [],
			dealPageIndex: 1,
			dealPageSize: 8,
			dealPageTotal: 0,
			dealTotalInfo: 0,
			infoForm: {
				token: "",
			},
			outForm: {
				inHospitalLog: 0,
				index: 0,
				flag: 2,
			},
			moneyOutFlag: false,
			moneyOutFlag2: false,
			patientMoney: 0,
        }
    },
	computed: {
		...mapState(['token'])
	},

    methods: {
		exportData() {
			this.infoForm.token = this.$store.state.token;
			exportDealInfo(this.infoForm).then(resp => {
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
		getDeal(pageIndex, pageSize){
			this.showDealFlag = true;
			getDealInfo(pageIndex, pageSize, this.$store.state.token).then(resp =>{
				this.dealPageInfos = resp.data.data;
				this.dealPageIndex = resp.data.pageIndex;
				this.dealPageSize =  resp.data.pageSize;
				this.dealPageTotal = resp.data.pageTotal;
				this.dealTotalInfo = resp.data.count;
				
			})
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
		getMedicineInfo(pageIndex, pageSize, index) {
			this.medicalAdvice = this.MedicalInfos[index];
			this.oid = this.medicalAdvice.oid;
			this.showMedicineFlag = true;
			this.loading = true;
			this.index = index;
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
			this.showInspectDetailflag = true;
			this.loading = true;
			this.index = index;
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
		
		showUpdBedsWin() {
				
				getAvailableBedsInfo(this.inhosPageInfos[0].departmentId).then(resp => {
					this.availableBeds = resp.data;
				});
				this.showBedFormflag = true;
			
		},
		completeInhosBeds() {
			upcompleteInhospital(this.bedForm).then(() => {
				this.$message({
				    message: '修改床位申请已提交！',
				    type: 'success'
				});
				
				this.showBedFormflag = false;
				this.$router.push("/inhos");
			});
		},
        /*  获取当前用户的住院表单 */
		getinhosPageInfo(pageIndex, pageSize) {
			
			getPageUserHospitalization(pageIndex, pageSize, this.$store.state.token).then(resp => {
				
				this.bedForm = resp.data.data;
				this.inhosPageInfos = resp.data.data;
				this.inhosPageIndex = resp.data.pageIndex;
				this.inhosPageSize =  resp.data.pageSize;
				this.inhosPageTotal = resp.data.pageTotal;
				this.inhosTotalInfo = resp.data.count;
				
				this.loading = false;

				if(this.inhosPageInfos[0].status == "待入院"){
					this.active = 1;
				}
				if(this.inhosPageInfos[0].status == "已入院"){
					this.active = 2;
					if(this.patientMoney > 0){
						this.active = 3;
					}
				}
			});
		},
		getDepartmentId(){
			
			getAvailableBedsInfo(this.inhosPageInfos[0].departmentId).then(resp => {
				this.availableBeds = resp.data;
			});
			this.showInhosDetailflag = true;
			this.originalBedId = this.inhosPageInfos[0].bedId;
		},	
		
		
		/** 提交住院表单 */
		completeInhospital(item){
			item.status = 2;
			item.originalBedId = this.originalBedId;
			upcompleteInhospital(item).then(() => {
				this.$message({
		            message: '提交住院信息成功！',
		            type: 'success'
		        });
				
				this.showInhosDetailflag = false;
				location.reload();
			});
		},
	   
	   
        /** 患者取消住院 */
       refuseInhospital(item){
       	if (this.refusechar == this.loginUser.name){
       		item.status = 0;
       		upcompleteInhospital(item).then(() => {
       			this.$message({
       		        message: '已经为您取消入院:<',
       		        type: 'warning'
       		    });
       			this.refuseFlag=false;
       			this.$router.push("/user");
       		});
       	} else {
       		this.$message({
       			message: '操作失败 名字输入错误',
       			type: 'error'
       		});
       		this.refuseFlag=false;
       		this.$router.push("/user");
       	}
           
       },

		
		/** 患者电子钱包部分 */
		/** 获取患者电子账户余额 */
		getPatientMoneyInfo(){
			getMoneyInfo(this.$store.state.token).then(resp => {
				this.patientMoney = resp.data;
		})
		},


        /** 完成充值，增加患者电子账户余额 */
        completeAddmoney(){
			this.newForm.token =this.$store.state.token
			upaddpatientmoney(this.newForm).then(()=>{
			this.$message({
			message: '充值成功:)',
			type: 'success'
			});

			this.addmoneyflag = false;
			location.reload();
			})
		},
		

		/** 医嘱记录部分 */
		/** 获取患者的全部医嘱记录 */
		getMedicalInfos(pageIndex, pageSize) {
			this.oid = '';
			this.type = '1';
			getPageMedicalInfos(pageIndex, pageSize, this.$store.state.token, this.patientName, this.oid, this.type).then(resp => {
				
				this.MedicalInfos = resp.data.data;
				this.MedicalPageIndex = resp.data.pageIndex;
				this.MedicalPageSize =  resp.data.pageSize;
				this.MedicalPageTotal = resp.data.pageTotal;
				this.MedicalTotalInfo = resp.data.count;
			});
		},

		completeMinusmoney(){
			this.newForm.token =this.$store.state.token
			upminuspatientmoney(this.newForm).then(()=>{
			this.$message({
			message: '提现成功:)',
			type: 'success'
			});
		
			this.minusmoneyflag = false;
			location.reload();
			})
		},
		
		outhospital(id){
			this.outForm.inHospitalLog = id;
			getMoneyInfo(this.$store.state.token, id).then(resp =>{
				this.patientMoney = resp.data;
			});
			
			if (this.patientMoney < 0){
				this.moneyOutFlag = true;
			}

			else if(this.patientMoney > 0){
				this.moneyOutFlag2 = true;
			}
			
		},
		
		commitOut(){
			this.outForm.flag = 2;
			upOuthospital(this.outForm).then(resp =>{
				this.$message({
				    message: '出院成功！',
				    type: 'success'
				});
				
				this.moneyOutFlag2 = false;
				location.reload();
			});
		},

	
    },


    mounted(){
		getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		this.getPatientMoneyInfo();
        this.getinhosPageInfo(1, this.inhosPageSize);
		this.getMedicalInfos(1, this.MedicalPageSize);
    }
}
</script>
