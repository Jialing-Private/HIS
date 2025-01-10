<template>
    <div>
		<div class="mybody">
        
			<el-image class="user-img" :src="require('@/assets/inhos.svg')"></el-image>

            <div class="user-info">
				<el-descriptions style="background-color: #FFFFFF; padding: 15px;" title="个人资料" :column="1" border>
					<template slot="extra">
						<el-button @click="showUpdUserWin" type="primary" size="small">修改</el-button>
					</template>
					<template slot="extra">
						<el-button @click="deleteFlagWin" type="danger" size="small">注销</el-button>
					</template>
				    <el-descriptions-item label="用户姓名">{{loginUser.name}} </el-descriptions-item>
					<el-descriptions-item label="用户性别">{{loginUser.gender}} </el-descriptions-item>
				    <el-descriptions-item label="身份证号">{{loginUser.idNumber}}</el-descriptions-item>
				    <el-descriptions-item label="联系电话">{{loginUser.phone}}</el-descriptions-item>
				    <el-descriptions-item label="用户年龄">{{loginUser.age}}</el-descriptions-item>
				    <el-descriptions-item label="注册时间">{{loginUser.createTime}}</el-descriptions-item>
				    <el-descriptions-item label="联系地址">{{loginUser.address}}</el-descriptions-item>
				</el-descriptions>
			</div>

			<div class="regi-logs">
				<el-row :gutter="80">
					<el-card style="margin-bottom: 15px;" v-show="inhosTotalInfo > 0">
						<div slot="header">
							<span class="el-icon-s-grid"></span> 住院通知
						</div>
						<div>
							<el-row v-if="inhosTotalInfo > 0" :gutter="15">
								<template v-for="item in inhosPageInfos">
									<el-col :span="24">
										<div class="register-panel">

											<div class="register-icon">
												<span class="el-icon-s-order"></span>
											</div>

											<div class="register-title">
												<span class="register-doctor-name">电子住院单</span>
											</div>

											<div class="register-detail">
												<span class="register-detail-item">主治医师：{{ item.doctorName }}</span>
												<span class="register-detail-item">开单日期：{{ item.createTime }} </span>
											</div>

											<div class="Inhospital-change-icon" v-if="item.status=='待入院'">
												<el-button @click="getDepartmentId" type="primary" size="small">入院登记</el-button>
											</div>

											<div class="Inhospital-yes-icon" v-if="item.status=='待入院'">
												<el-button @click="refuseFlag=true" type="danger" size="small">撤销入院</el-button>
											</div>
											
											<div class="Inhospital-change-icon" v-if="item.status=='已入院'">
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
									<el-dialog title="电子住院单" width="700px" :visible.sync="showInhosDetailflag">
										<el-form label-width="110px" :model="userForm">
											<el-row :gutter="15">
									            <el-col :span="12">
									                <el-form-item label="患者姓名">
									                    <el-input v-model="item.patientName" :disabled="true" auto-complete = "off"></el-input>
									                </el-form-item>
									            </el-col>
									            <el-col :span="12">
									                <el-form-item label="住院科室">
									                    <el-input v-model="item.doctorDepartmentName" :disabled="true"></el-input>
									                </el-form-item>
									            </el-col>
									        </el-row>

											<el-row :gutter="15">
									            <el-col :span="12">
									                <el-form-item label="主治医师">
									                    <el-input v-model="item.doctorName" :disabled="true" auto-complete = "true"></el-input>
									                </el-form-item>
									            </el-col>
									            <el-col :span="12">
									                <el-form-item label="住院单开具时间">
									                    <el-input v-model="item.createTime" :disabled="true" auto-complete = "true"></el-input>
									                </el-form-item>
									            </el-col>
									        </el-row>

											<el-row :gutter="15">
												<el-form-item label="选择入院时间">
													<el-date-picker
													class="datestyle"
													v-model="item.hospitalizationStartTime"
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
													<el-select style="width:100%;" v-model="item.bedId" placeholder="请选择科室">
														<el-option label="查看全部" value=""></el-option>
														<el-option v-for="(item, index) in availableBeds"
															:key="index" :label="item.info" :value="item.id"></el-option>
													</el-select>
												</el-form-item>
											</el-row>
											<el-form-item size="mini">
												<el-button type="primary" @click="completeInhospital(item)">确认入院</el-button>
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
								</template>
							</el-row>
							<el-empty v-else description="暂无相关记录"></el-empty>
						</div>
					</el-card>

					<el-card style="margin-top: 15px;">
						<div slot="header">
							<span class="el-icon-s-grid"></span>  挂号预约记录
						</div>

						<div>
							<el-row v-if="totalInfo > 0"  :gutter="15">
								<template v-for="item in pageInfos">
									<el-col :span="8">
										<div class="register-panel">
											<div class="register-icon">
												<span class="el-icon-s-claim"></span>
											</div>
											<div class="register-title">
												<span class="register-doctor-name">{{ item.doctorName }}</span>
												<span class="register-doctor-desc">{{ item.doctorJob }}</span>
												<span class="register-doctor-desc">{{ item.doctorDepartmentName }}</span>
											</div>
											<div class="register-detail">
												<span class="register-detail-item">预定时间：{{ item.registerTime }}</span>
												<span class="register-detail-item">挂号费用：{{ item.registerFee }} 元</span>
											</div>
										</div>
									</el-col>
								</template>
							</el-row>
							<el-empty v-else description="暂无相关记录"></el-empty>
							<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
								@current-change="handleCurrentChange" :current-page="pageIndex"
								:page-size="pageSize" layout="total, prev, pager, next" :total="totalInfo">
							</el-pagination>
						</div>
					</el-card>
					<el-card style="margin-top: 15px;" v-show="presTotalInfo">
						<div slot="header">
							<span class="el-icon-s-grid"></span> 历史处方
						</div>
						<div>
							<el-row v-if="presTotalInfo > 0"  :gutter="15">
								<template v-for="item in presInfos">
									
										<el-col :span="8">
											<div class="his-pres-panel">
												<div class="register-icon">
													<span class="el-icon-tickets"></span>
												</div>
												<div class="register-title">
													<span class="register-doctor-name">{{ item.doctorName }}</span>
													<span class="register-doctor-desc">{{ item.doctorJob }}</span>
													<span class="register-doctor-desc">{{ item.doctorOfficeName }}</span>
												</div>
												<div class="register-detail">
													<span class="register-detail-item">制定时间：{{ item.presTime }}</span>
												</div>
											</div>
										</el-col>
										<el-col :span="4">
											
											<el-button  @click="readPres(item)" type="success">查看处方</el-button>
												
				   						</el-col>
				   					
								</template>
							</el-row>
							<el-empty v-else description="暂无相关记录"></el-empty>
						</div>
						<el-pagination v-if="presPageTotal > 1" 
							style="margin-top: 15px;" 
							@size-change="handlePresSizeChange"
							@current-change="handlePresCurrentChange" 
							:current-page="presPageIndex"
							:page-size="presPageSize" layout="total, prev, pager, next" :total="presTotalInfo">
						</el-pagination>
					</el-card>

					<el-dialog title="门诊处方" width="1000px" :visible.sync="showPresInfoFlag" :close-on-click-modal="false">
						<el-form label-width="200px">
							<el-row :gutter = "15">
								<el-col :span="12">
									<el-form-item>
										<span slot="label">
											<span>医嘱开具医师：</span>
										</span>
										<span>{{ medicalAdvice.startDoctorName }}</span>
									</el-form-item>
								</el-col>
								<el-col :span="12">
									<el-form-item>
										<span slot="label">
											<span>医嘱号：</span>
										</span>
										<span>{{ medicalAdvice.oid }}</span>
									</el-form-item>
								</el-col>
							</el-row>
							<el-row :gutter = "15">
								<el-col :span="12">
									<el-form-item>
										<span slot="label">
											<span>医嘱内容：</span>
										</span>
										<span>{{ medicalAdvice.content }}</span>
									</el-form-item>
								</el-col>
							</el-row>
							<el-row :gutter = "15">
								<el-col :span="12">
									<el-form-item>
										<span slot="label">
											<span>处方时间：</span>
										</span>
										<span>{{ medicalAdvice.time }}</span>
									</el-form-item>
								</el-col>
							</el-row>
							
							<el-card shadow="never">
								<div>
									<el-table v-loading="loading" stripe
										element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
										element-loading-background="rgba(124, 124, 124, 0.8)" :data="MedicineInfos" border>
											<el-table-column align="center" type="index" ></el-table-column>
											<el-table-column align="center" prop="medicine" label="药物名称"></el-table-column>
											<el-table-column align="center" prop="dose" label="给药量" :show-overflow-tooltip="true"></el-table-column>
											<el-table-column align="center" prop="medication" label="用药方式" :show-overflow-tooltip="true"></el-table-column>
											<el-table-column align="center" prop="freq" label="用药频率" :show-overflow-tooltip="true"></el-table-column>
											<el-table-column align="center" prop="fee" label="单项价格" :show-overflow-tooltip="true"></el-table-column>
									</el-table>
									<!-- <el-pagination v-if="MedicinePageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
										@current-change="handleCurrentChange" :current-page="MedicineIndex" :page-sizes="[10, 20, 50]"
										:page-size="MedicinePageSize" layout="total, sizes, prev, pager, next, jumper" :total="MedicineTotalInfo">
									</el-pagination> -->
								</div>
							</el-card>
							<el-row :gutter = "15">
								<el-col :span="12">
									<el-form-item>
										<span slot="label">
											<span>药品总价：</span>
										</span>
										<span>{{ medicalAdvice.totalprice }}</span>
									</el-form-item>
								</el-col>
							</el-row>
						</el-form>
						<div slot="footer" class="dialog-footer">
							<el-button @click="showPresInfoFlag = false">关闭</el-button>
						</div>
					</el-dialog>
					<el-card style="margin-top: 15px;">
					    <div slot="header">
							<span class="el-icon-s-grid"></span> 检验报告
						</div>
					    <div>
							<el-row v-if="repoTotalInfo > 0"  :gutter="15">
								<template v-for="item in repoInfos">
									<el-col :span="8">
										<div class="his-pres-panel">
											<div class="register-icon">
												<span class="el-icon-tickets"></span>
											</div>
											<div class="register-title">
												<span class="register-doctor-name">{{ item.checkItem }}</span>
											</div>
											<div class="register-detail">
												<span class="register-detail-item">检验时间：{{ item.checkTime }}</span>
												<span class="register-detail-item">报告时间：{{ item.repoTime }}</span>
											</div>
										</div>
									</el-col>
									<el-col :span="4">
										
											<el-button  @click="readRepo()" type="success">查看报告</el-button>
									
			   						</el-col>
								</template>
							</el-row>
							<el-empty v-else description="暂无相关记录"></el-empty>
						</div>
						<el-pagination v-if="repoPageTotal > 1" 
							style="margin-top: 15px;" 
							@size-change="handleRepoSizeChange"
							@current-change="handleRepoCurrentChange" 
							:current-page="repoPageIndex"
							:page-size="repoPageSize" layout="total, prev, pager, next" :total="repoTotalInfo">
					</el-pagination>
					</el-card>
					<el-dialog title="检验报告" width="1100px" :visible.sync="showRepoFlag">
				    	<div class="report-img"></div>
				    	<div slot="footer" class="dialog-footer">
							<el-button type="primary" @click="closeRepo()">关 闭</el-button>
						</div> 
				    </el-dialog>
				</el-row>
			</div>
		</div>



		<el-dialog title="患者信息编辑" width="700px" :visible.sync="showUpdUserFlag">
			<el-form label-width="90px" :model="userForm">
				<el-form-item label="身份证号">
				    <el-input v-model="userForm.idNumber"
				                placeholder="请输入身份证号…" autocomplete="off"></el-input>
				</el-form-item>
				<el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户账号">
		                    <el-input v-model="userForm.userName"
		                                placeholder="请输入用户账号…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="用户密码">
		                    <el-input v-model="userForm.passWord" type="password"
		                                placeholder="请输入用户密码…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		        </el-row>
		        <el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户姓名">
		                    <el-input v-model="userForm.name"
		                                placeholder="请输入用户姓名…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="联系电话">
		                    <el-input v-model="userForm.phone"
		                            placeholder="请输入联系电话…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		        </el-row>
		        <el-row :gutter="15">
		            <el-col :span="12">
		                <el-form-item label="用户年龄">
		                    <el-input v-model="userForm.age"
		                                placeholder="请输入用户年龄…" autocomplete="off"></el-input>
		                </el-form-item>
		            </el-col>
		            <el-col :span="12">
		                <el-form-item label="用户性别">
		                    <el-radio-group v-model="userForm.gender">
		                        <el-radio label="男"></el-radio>
		                        <el-radio label="女"></el-radio>
		                    </el-radio-group>
		                </el-form-item>
		            </el-col>
		        </el-row>
		        <el-form-item label="联系地址">
					<el-input v-model="userForm.address" type="textarea"
		                      rows="6" placeholder="请输入联系地址…" autocomplete="off"></el-input>
				</el-form-item>
		    </el-form>

			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdUserFlag = false">取 消</el-button>
				<el-button type="primary" @click="updLoginUser()">确 定</el-button>
			</div>
		</el-dialog>
		<el-dialog title="注销账号" width="700px" :visible.sync="deleteFlag3">
			<el-form label-width="0px">
				<el-form-item  v-if="this.inhosTotalInfo == 0">
				    <span style="font-family: 宋体;font-size: 5ch;color: green;">当前无正在进行的住院记录，可以注销</span>
				</el-form-item>
				<el-form-item  v-else-if="this.inhosTotalInfo > 0">
				    <span style="font-family: 宋体;font-size: 5ch;color: royalblue;">当前有正在进行的住院记录，不能注销</span>
				</el-form-item>
		    </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="deleteFlag3 = false" type="info">取 消</el-button>
				<el-button v-if="this.inhosTotalInfo == 0 & this.flag == 0" type="primary" :disabled="abledBut">{{ setTimeNum }}s</el-button>
				<el-button v-if="this.inhosTotalInfo == 0 & this.flag == 1" type="primary" @click="nextStep2">下一步</el-button>
			</div>
		</el-dialog>
		<el-dialog title="注销账号" width="700px" :visible.sync="deleteFlag">
			<el-form label-width="0px">
				<el-form-item  v-if="this.deleteForm.patientMoney == 0">
				    <span style="font-family: 宋体;font-size: 5ch;color: green;">当前账号余额{{ this.deleteForm.patientMoney }}元，可以注销</span>
				</el-form-item>
				<el-form-item  v-else-if="this.deleteForm.patientMoney > 0">
				    <span style="font-family: 宋体;font-size: 5ch;color: royalblue;">当前账号余额{{ this.deleteForm.patientMoney }}元，不能注销</span>
				</el-form-item>
				<el-form-item  v-else>
				    <span style="font-family: 宋体;font-size: 5ch;color: black;">当前账号余额</span><span style="font-family: 宋体;font-size: 5ch;color: red;">{{ this.deleteForm.patientMoney }}</span><span style="font-family: 宋体;font-size: 5ch;color: black;">元，禁止注销</span>
					<br><span style="font-family: 宋体;font-size: 5ch;color: red;">请尽快补缴欠费账单</span></br>
				</el-form-item>
		    </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="deleteFlag = false" type="info">取 消</el-button>
				<el-button v-if="this.deleteForm.patientMoney == 0 & this.flag == 0" type="primary" :disabled="abledBut">{{ setTimeNum }}s</el-button>
				<el-button v-if="this.deleteForm.patientMoney == 0 & this.flag == 1" type="primary" @click="nextStep">下一步</el-button>
			</div>
		</el-dialog>
		<el-dialog title="注销账号" width="700px" :visible.sync="deleteFlag2">
				<div style="height: 480px;" class="scrollbar">
					
				<span style="font-family: 宋体;font-size: 3ch;color: red;">请阅读以下注销协议后确认注销：</span>
				<el-scrollbar style="height: 100%;">
				<p>用户注销协议</p>
				<p>在您注销您的帐号之前，请充分阅读、理解并同意下列事项：</p>
				
				<p>1. 注销须知</p>
				<p>如果您申请注销帐号，请在提交申请前确认以下信息，以保证您的帐号和财产安全：</p>
				
				<p>1.1. 您的帐号处于正常使用状态，未发生过被盗、其他帐号异常情形等；</p>
				
				<p>1.2. 帐号内财产已结清。 包括：您的电子钱包（提现路径： 住院信息 > 提现）已清空。</p>
				
				<p>1.3. 住院信息无任何未出院的情况。</p></p>
				
				<p>1.4 帐号未涉及任何争议纠纷。</p>
				
				<p>2. 注销流程</p>
				<p>不卜庐医院信息系统提供自助注销方式。</p>
				
				<p>PC 端：个人中心 > 注销。</p>
				
				<!-- <p>如果注销过程中有任何问题，可在 关于 > 反馈 或 关于 > 联系客服 解决</p> -->
				
				<p>3. 特别提醒</p>
				<p>3.1 您的帐号一旦被注销成功将不可恢复，您将无法再使用本帐号或找回您添加、绑定的任何本帐号内容或信息，包括但不限于：</p>
				<p>3.1.1 您帐号下的个人资料（用户名、实名认证信息、身份认证信息等）。请您务必在注销之前自行备份与帐号相关的前述所有内容或信息。您理解并同意，不卜庐也无法协助您恢复前述内容或信息。</p>
				
				<p>3.2 您知晓并同意，如不卜庐医院信息系统帐号存在权属争议的，本院有权禁用该帐号，直至争议双方通过和解或司法途径解决并向本院提供有效证明。在此期间本院有权拒绝帐号注销操作。</p>
				
				<p>3.3 注销不卜庐医院信息系统不卜庐医院信息系统帐号并不代表帐号注销前的行为和相关责任得到任何形式的豁免或减轻。</p>
				
				<p>3.4 注销成功后，我们将删除您的个人信息或对其进行匿名化处理。请您知悉并理解，根据相关法律法规规定，本医院将就相关日志记录保留不少于 6 个月的时间。</p>
					</el-scrollbar>
				</div>
			<div slot="footer" class="dialog-footer">
				<el-button @click="deleteFlag2 = false">取 消</el-button>
				<el-button v-if="this.flag2 == 0" type="danger" :disabled="abledBut2">{{ setTimeNum2 }}s</el-button>
				<el-button v-if="this.flag2 == 1" type="danger" @click="deleteUser">确认</el-button>
			</div>
		</el-dialog>
	</div>

</template>

<style></style>

<script>
import {
	exit,
	getStatis,
	getLoginUser,
	updLoginUserInfo,
    getPageRegistes,
	getPageUserHospitalization,
	upcompleteInhospital,
	getMoneyInfo,
	getAvailableBedsInfo,
	delPatientUserInfo,
	getPagePreses,
	getPageRepos,
	getPresInfo,
} from "../api";
import { mapState } from "vuex";
export default {
    data() {
        var checkOldPwd = async (rule, value, callback) => {
            if (value) {
                await checkUserPwd(this.$store.state.token, value).then((resp) => {
                    if (resp.code != 0) {
                        callback(new Error("原始密码输入错误"));
                    }
                });
            } else {
                callback(new Error("原始密码必须"));
            }
            callback();
        };
        var checkNewPwd = (rule, value, callback) => {
            if (!value) {
                callback(new Error("修改密码必须输入"));
            }

            callback();
        };
        var checkRePwd = (rule, value, callback) => {
            if (!value) {
                callback(new Error("确认密码必须输入"));
            }

            if (value != this.userPwd.newPwd) {
                callback(new Error("两次输入密码不一致"));
            }

            callback();
        };
		
		let _this = this;

        return {
			originalBedId: "",
			availableBeds: [],
			loginUser: {},
			statisInfo: {},
            pageInfos: [],
            pageIndex: 1,
			refusechar: "",
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,
			inhosPageInfos: 0,
			inhosPageIndex: 1,
			inhosPageSize: 12,
			inhosPageTotal: 0,
			inhosTotalInfo: 0,
            showUpdUserFlag: false,
			refuseFlag: false,
			deleteFlag: false,
			deleteFlag2: false,
			deleteFlag3: false,
			deleteForm: {
				patientMoney: 0,
			},
			abledBut: false,
			setTimeNum: 3,
			timeWrap: null,
			abledBut2: false,
			setTimeNum2: 5,
			timeWrap2: null,
			flag: 0,
			flag2: 0,

            userForm: {
				id: '',
				idNumber: '',
                address: '',
                userName: '',
                passWord: '',
                name: '',
                gender: '',
                age: '',
                phone: '',
                type: 2,
            },

			hospitalizationForm: {
				id: "",
				patientId: '',
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

			hospitalizationFlag: false,
			showInhosDetailflag: false,
			showInhosDetailflag2: false,
			resForm: {
				nowDate: "",
				setNowDate: "",
			},


			// 处方和检查记录
			loading: true,
			showRepoFlag: false,
        	showPresFlag: false,
        	// repoInfos应包含检验项目，检验时间，报告时间三项内容
            repoInfos: [],
            // presInfos应包含医生姓名，医生职位，科室名称，制定时间，药品名称，药品剂量，服用频率七项内容
            presInfos: [],
            repoPageIndex: 1,
            repoPageSize: 6,
            repoPageTotal: 0,
            repoTotalInfo: 0,
            presPageIndex: 1,
            presPageSize: 6,
            presPageTotal: 0,
            presTotalInfo: 0,
			showPresInfoFlag: false,

			medicalAdvice:{},
			MedicineInfos:[],



			DisableDatesOption: {
				disabledDate(time) {
					_this.resForm.setNowDate = _this.resForm.nowDate;
					let curDate = (new Date()).getTime();
					let pre = new Date();
					let oneday = curDate - 24 * 3600 * 1000;
					let thirtyonedays = 31 * 24 * 3600 * 1000;
					let oneMonth = curDate + thirtyonedays;
					return time.getTime() < oneday || time.getTime() > oneMonth;
				}
			},
        }
    },
	watch: {
	    setTimeNum (newVal, oldVal) {
	      if (newVal < 0) {
	        clearInterval(this.timeWrap)
	        this.abledBut = false
	        this.setTimeNum = 3
			this.flag = 1
	      }
	    },
		setTimeNum2 (newVal, oldVal) {
		  if (newVal < 0) {
		    clearInterval(this.timeWrap2)
		    this.abledBut2 = false
		    this.setTimeNum2 = 5
			this.flag2 = 1
		  }
		}
	  },

	computed: {
		...mapState(['token'])
	},
    methods: {
		deleteFlagWin(){
			this.flag = 0
			this.setTimeNum = 3
			this.deleteFlag3 = true;
			this.getSecond();
		},
		getSecond() {
			let _this = this;
			this.timeWrap = setInterval(function(){
				_this.setTimeNum--;
				if (_this.setTimeNum === 0){
					clearInterval(_this.setTimeNum);
					this.abledBut = true
					this.flag = 1
			}
		}, 1000)
	},
	getSecond2() {
			let _this = this;
			this.timeWrap2 = setInterval(function(){
				_this.setTimeNum2--;
				if (_this.setTimeNum2 === 0){
					clearInterval(_this.setTimeNum2);
					this.abledBut2 = true
					this.flag2 = 1
			}
		}, 1000)
	},
		nextStep() {
			this.flag2 = 0;
			this.flag = 0;
			this.setTimeNum2 = 5;
			this.deleteFlag = false;
			this.deleteFlag2 = true;
			this.getSecond2();
		},
		nextStep2() {
			this.flag2 = 0;
			this.flag = 0;
			this.setTimeNum2 = 5;
			this.deleteFlag3 = false;
			this.deleteFlag = true;
			this.getSecond2();
		},
		getPatientMoneyInfo(){
			getMoneyInfo(this.$store.state.token).then((resp) => {
				this.deleteForm.patientMoney = resp.data;
		})
		},
		deleteUser(){
		
		    delPatientUserInfo(this.$store.state.token).then(() =>{
		
		        this.deleteFlag2 = false;
				exit(this.$store.state.token).then(() => {
					this.$store.commit("clearToken");
					sessionStorage.clear();
					this.$router.push("/welcome");
					location.reload();
					this.$message({
						message: '注销成功',
						type: 'success'
					})
				});
		    });
		},
					

		
		handleSizeChange(pageSize){
		
			this.getPageInfo(1, pageSize);
		},
		handleCurrentChange(pageIndex){
		
			this.getPageInfo(pageIndex, this.pageSize);
		},

        showUpdUserWin(){

            getLoginUser(this.$store.state.token).then(resp =>{

                this.userForm = resp.data;
        		this.userForm["token"] = this.$store.state.token;
                this.showUpdUserFlag = true;
            });
        },

		showInhosDetail(){
			this.showInhosDetailflag = true;
		},


        updLoginUser(){

            updLoginUserInfo(this.userForm).then(() =>{

                this.$message({
                    message: '修改个人信息成功',
                    type: 'success'
                });

                this.showUpdUserFlag = false;

        		this.$router.push("/user");
            });
        },

        getPageInfo(pageIndex, pageSize) {

            getPageRegistes(pageIndex, pageSize, this.$store.state.token).then(resp => {

                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;

                this.loading = false;
            });
        },

		/*  获取当前用户的住院表单 */
		getinhosPageInfo(pageIndex, pageSize) {

			getPageUserHospitalization(pageIndex, pageSize, this.$store.state.token).then(resp => {

				this.inhosPageInfos = resp.data.data;
				this.inhosPageIndex = resp.data.pageIndex;
				this.inhosPageSize =  resp.data.pageSize;
				this.inhosPageTotal = resp.data.pageTotal;
				this.inhosTotalInfo = resp.data.count;

				this.loading = false;

			});
		},

		/** 提交住院表单 */
		completeInhospital(item){
			item.status = 2,
			item.originalBedId = this.originalBedId,
			upcompleteInhospital(item).then(() => {
				this.$message({
                    message: '提交住院信息成功！',
                    type: 'success'
                });

				this.showInhosDetailflag = false;
				this.$router.push("/user");
			});
		},
		
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

		getDepartmentId(){

			getAvailableBedsInfo(this.inhosPageInfos[0].departmentId).then(resp => {
				this.availableBeds = resp.data;
			});
			this.showInhosDetailflag = true;
			this.originalBedId = this.inhosPageInfos[0].bedId;
		},


        handleSizeChange(pageSize){

            this.getPageInfo(1, pageSize);
        },


        handleCurrentChange(pageIndex){

            this.getPageInfo(pageIndex, this.pageSize);
        },



        // 处方和检查报告
        getRepoPageInfo(pageIndex, pageSize) {

            getPageRepos(pageIndex, pageSize, this.$store.state.token).then(resp => {

                this.repoInfos = resp.data.data;
                this.repoPageIndex = resp.data.pageIndex;
                this.repoPageSize = resp.data.pageSize;
                this.repoPageTotal = resp.data.pageTotal;
                this.repoTotalInfo = resp.data.count;

                this.loading = false;
            });
        },
		readPres(item){

            getPresInfo(item).then(resp =>{

                this.MedicineInfos = resp.data.MedicineInfos;
				this.medicalAdvice = resp.data.medicalAdvice;
                this.showPresInfoFlag = true;
            });
        
        },
        handleRepoSizeChange(pageSize){

            this.getRepoPageInfo(1, pageSize);
        },
        handleRepoCurrentChange(pageIndex){

            this.getRepoPageInfo(pageIndex, this.pageSize);
        },
        // 获取电子处方页面信息
        getPresPageInfo(pageIndex, pageSize) {

            getPagePreses(pageIndex, pageSize, this.$store.state.token).then(resp => {

                this.presInfos = resp.data.data;
                this.presPageIndex = resp.data.pageIndex;
                this.presPageSize = resp.data.pageSize;
                this.presPageTotal = resp.data.pageTotal;
                this.presTotalInfo = resp.data.count;

                this.loading = false;
            });
        },
        handlePresSizeChange(pageSize){

            this.getPresPageInfo(1, pageSize);
        },
        handlePresCurrentChange(pageIndex){

            this.getPresPageInfo(pageIndex, this.pageSize);
        },

        //查看报告详情
        readRepo(){

        	this.showRepoFlag = true
        },

        closeRepo(){

        	this.showRepoFlag = false
        },

    },



    mounted(){

		getLoginUser(this.$store.state.token).then(resp =>{

			this.loginUser = resp.data;
		});

		getStatis().then(resp =>{

			this.statisInfo = resp.data;
		});
		this.getPatientMoneyInfo();

		this.getPageInfo(1, 12);

		this.getinhosPageInfo(1, 12);
		
		this.getRepoPageInfo(1, this.repoPageSize);
        this.getPresPageInfo(1, this.presPageSize);
		
    }
}
</script>
