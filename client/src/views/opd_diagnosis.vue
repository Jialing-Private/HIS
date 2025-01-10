<template>
	<div>
		<div>
			<el-col :span="8" gutter="15">
				<div class="button-container">
					<el-button @click="showQueue()" type="primary" class="queue-infos-button">排队信息</el-button>
				</div>
				<div class="patient-info-panel">
					<div v-if="onePatient">
						<div class="patient-info-title">患者信息</div>
						<div class="patient-img"></div>
						<div class="patient-info-details">患者姓名: {{onePatient.name}}</div>
						<div class="patient-info-details">患者性别: {{onePatient.gender}}</div>
						<div class="patient-info-details">患者年龄: {{onePatient.age}}</div>
					</div>
					<el-empty v-else description="队列中暂无病人"></el-empty>
					<el-button @click="sentHospital()" type="primary" class="sent-hospital-button">开具住院单</el-button>
				</div>
				
			</el-col>
		</div>
		<div>
			<el-col :span="16">
				<div class="operating-area">
					<div class="steps-panel">
						<el-steps :active="active" finish-status="success" class="steps-style">
							<el-step title="患者症状"></el-step>
							<el-step title="检验单开具"></el-step>
							<el-step title="病情诊断"></el-step>
							<el-step title="处方开具"></el-step>
						</el-steps>
					</div>
					<div class="diagnosis-area">
						<div v-if="active==0">
							<div class="diagnosis-step-label">患者症状</div>
							
							<el-input
								type="textarea"
								:autosize="{ minRows: 10, maxRows: 20}"
								v-model="symptom"
								class="diagnosis-step-symptom">
							</el-input>
							
							<el-button @click="toCheckStep()" type="primary" class="diagnosis-step-next">下一步</el-button>
							
						</div>
						
						<div v-else-if="active==1">
							<div class="diagnosis-step-label">检验单开具</div>
							<div class="one-pres">
								<el-form :inline="true" :model="checkForm" ref="checkForm" class="pres-form-inline">
									<el-form-item 
										v-for="(oneCheck, index) in checkForm.medicine_forms"
										:label="'检验项目' + (index + 1)"
										class="one-pres-box"
										:key="oneCheck.key"
										>
										<el-form-item label="检验名称" class="one-pres-item">
			    							<el-input v-model="oneCheck.inspectName" placeholder="检验名称" class="one-pres-input"></el-input>
			  							</el-form-item>
			  							<el-form-item>
			  								<el-button type="info" class="delete-one-pres" @click="removeCheck(oneCheck)">删除项目</el-button>
			  							</el-form-item>
			  						</el-form-item>
		  						</el-form>
		  					</div>  
							<div>
								<el-button type="primary" @click="addCheck()" class="add-pres-button">增加检验单项目</el-button>
								<el-button @click="resetCheck()" type="warning">重置</el-button>
							</div>
							<div class="diagnosis-step-next">
								<el-button @click="toSympStep()">上一步</el-button>
								<el-button @click="confirmCheck()" type="primary">确认检验单</el-button>
								<el-button @click="toDiagStep()" type="info">跳 过</el-button>
							</div>
						</div>

						<div v-else-if="active==2">
						
							<div class="diagnosis-step-label">病情诊断:</div>
							
							<el-input
								type="textarea"
								:autosize="{ minRows: 10, maxRows: 20}"
								v-model="diagnosis"
								class="diagnosis-step-symptom">
							</el-input>
							
							
							<el-button @click="toPresStep()" class="diagnosis-step-next" type="primary">下一步</el-button>
							<el-button @click="toCheckStep()" class="diagnosis-step-next">上一步</el-button>
							
						</div>

						<div v-else-if="active==3">
							<div class="diagnosis-step-label">处方开具</div>
							<div class="one-pres">
								<el-form :inline="true" :model="presForm" ref="presForm" class="pres-form-inline">
									<el-form-item label="医嘱">
										<el-input 
											type="textarea"
											:autosize="{ minRows: 3, maxRows: 5}"
											class="diagnosis-pres-content" 
											v-model="presForm.content"></el-input>
									</el-form-item>
									<el-form-item 
										v-for="(onePres, index) in presForm.medicine_forms"
										:label="'处方项目' + (index + 1)"
										class="one-pres-box"
										:key="onePres.key"
										>
										<el-form-item label="药品名称" class="one-pres-item">
			    							<el-input v-model="onePres.medicine" placeholder="药品名称" class="one-pres-input"></el-input>
			  							</el-form-item>
			  							<el-form-item label="用药方式" class="one-pres-item">
			    							<el-select v-model="onePres.medication" placeholder="用药方式" class="one-pres-input">
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
			  							<el-form-item label="用药疗程" class="one-pres-item">
											<el-input v-model="onePres.allFreq" placeholder="天" class="one-pres-input"></el-input>
										</el-form-item>
			  							<el-form-item label="用药频率" class="one-pres-item">
			  								<el-input v-model="onePres.freq" placeholder="天" class="one-pres-input"></el-input>
			  							</el-form-item>
			  							<el-form-item label="用药次数" class="one-pres-item">
			  								<el-input v-model="onePres.times" placeholder="次" class="one-pres-input"></el-input>
			  							</el-form-item>
			  							<el-form-item label="用药剂量" class="one-pres-item">
			  								<el-input v-model="onePres.dose" placeholder="每次" class="one-pres-input"></el-input>
			  							</el-form-item>
			  							<el-form-item>
			  								<el-button type="info" class="delete-one-pres" @click="removePres(onePres)">删除处方</el-button>
			  							</el-form-item>
			  						</el-form-item>
		  						</el-form>
		  					</div>  
							<div>
								<el-button type="primary" @click="addPres()" class="add-pres-button">增加处方项目</el-button>
								<el-button @click="resetPres()" type="warning">重置</el-button>
							</div>
							<div class="diagnosis-step-next">
								<el-button @click="toDiagStep()">上一步</el-button>
								<el-button type="primary" @click="confirmPres()">确认处方</el-button>
							</div>
							
						</div>
					</div>
				</div>
			</el-col>
		</div>
		<div>
			<el-dialog title="患者队列" width="1100px" :visible.sync="showQueueFlag">
		    	<div class="queue-info-table">
		    		<el-table :data="queueData">
		    			<el-table-column prop="name" label="患者姓名"></el-table-column>
		    			<el-table-column prop="gender" label="性别"></el-table-column>
		    			<el-table-column prop="updateTime" label="入队时间"></el-table-column>
		    		</el-table>
		    	</div>
		    	<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="closeQueue()">关 闭</el-button>
				</div> 
		    </el-dialog>
		</div>
		<div>
			<el-dialog title="检验单信息" :visible.sync="showCheckFlag" width="1300px">
		    	<div class="pres-info-table">
		    		<div>
			    		<div>单号: {{ checkForm.oid }}</div>
			    		<div>症状: {{ checkForm.symptom }}</div>
			    		<div>诊断: {{ checkForm.diagnosis }}</div>
			    		<div>医嘱: {{ checkForm.content }}</div>
			    		<div>医嘱类型: {{ checkForm.type }}</div>
			    		<div>挂号记录: {{ checkForm.registerLog }}</div>
			    		<div>开具医生: {{ checkForm.doctorId }}</div>
			    	</div>
		    		<el-table :data="checkForm.medicine_forms">
		    			<el-table-column prop="inspectName" label="检验项目"></el-table-column>
		    			<el-table-column prop="startTime" label="开具时间"></el-table-column>
		    		</el-table>
		    	</div>
		    	<div slot="footer" class="dialog-footer">
		    		<el-button type="primary" @click="submitCheck()">确 定</el-button>
					<el-button type="info" @click="closeCheck()">关 闭</el-button>
				</div> 
		    </el-dialog>
		</div>
		<div>
			<el-dialog title="处方信息" :visible.sync="showPresFlag" width="1300px">
		    	<div>
		    		<div>单号: {{ presForm.oid }}</div>
		    		<div>症状: {{ presForm.symptom }}</div>
		    		<div>诊断: {{ presForm.diagnosis }}</div>
		    		<div>医嘱: {{ presForm.content }}</div>
		    		<div>医嘱类型: {{ presForm.type }}</div>
		    		<div>挂号记录: {{ presForm.registerLog }}</div>
		    		<div>开具医生: {{ presForm.doctorId }}</div>
		    	</div>
		    	<div>
		    		<el-table :data="presForm.medicine_forms">
		    			<el-table-column prop="medicine" label="药品名称"></el-table-column>
		    			<el-table-column prop="medication" label="用药方式"></el-table-column>
		    			<el-table-column prop="allFreq" label="用药时长"></el-table-column>
		    			<el-table-column prop="startTime" label="开始时间"></el-table-column>
		    			<el-table-column prop="endTime" label="结束时间"></el-table-column>
		    			<el-table-column prop="freq" label="用药频率"></el-table-column>
		    			<el-table-column prop="times" label="用药次数"></el-table-column>
		    			<el-table-column prop="dose" label="用药剂量"></el-table-column>
		    		</el-table>
		    	</div>
		    	<div slot="footer" class="dialog-footer">
		    		<el-button type="primary" @click="submitPres()">确 定</el-button>
					<el-button type="info" @click="closePres()">关 闭</el-button>
				</div> 
		    </el-dialog>
		</div>
		<div>
			<el-dialog title="开具住院单" :visible.sync="showSentHosFlag" class="sent-to-hospital-diag">
		    	<el-row>确定为当前患者开具住院单？</el-row>
		    	<el-row>
		    		<div>患者编号: {{ inHosLog.patientId }}</div>
		    		<div>挂号编号: {{ inHosLog.registerId }}</div>
		    		<div>入院状态: {{ inHosLog.status }}</div>
		    	</el-row>
		    	<span slot="footer" class="dialog-footer">
		    		<el-button type="primary" @click="confirmSentHos()">确 定</el-button>
					<el-button type="info" @click="closeSentHos()">关 闭</el-button>
				</span> 
		    </el-dialog>
		</div>
	</div>
</template>

<style>
.el-header{
	font-size: 40px;
	text-align: center;
	position: relative;
}
	
</style>

<script>
import {
	getLoginUser,
	selectDoctorQueue,
	removeFromQueue,
	addToPres,
	sentToHos,
} from "../api";

export default {

	data(){

		return {

			showQueueFlag: false,
			showSentHosFlag: false,
			showPresFlag: false,
			showCheckFlag: false,
			loginUser:{},
			active: 0,

			queueData:[],
			// id 是预约记录编号，patient是患者编号，name是患者姓名
			onePatient: false,

			symptom: "",
			diagnosis: "",

			checkForm: {
				medicine_forms: [{
					inspectName:"",
				}],

			},

			presForm:{
				content:"",
				medicine_forms: [{
					medicine: "",
					medication: "",
					period: "",
					freq: "",
					times: "",
					dose: "",
					allFreq: "",
					},
				]
			},

			inHosLog: {},
		}
	},

	methods: {

		showQueue(){

			selectDoctorQueue(this.$store.state.token).then(resp =>{

				this.queueData = resp.data;
				if (this.queueData[0]) {

					this.onePatient = this.queueData[0];
				}else{

					this.onePatient = false;
				}
			});

			this.showQueueFlag = true;

		},
		closeQueue(){

			this.showQueueFlag = false;
		},

		// 步骤跳转
		toSympStep(){

			this.active = 0;
		},
		toCheckStep(){

			this.active = 1;
		},
		toDiagStep(){

			this.active = 2;
		},
		toPresStep(){

			this.active = 3;
		},
		// 检验单项目操作
		addCheck(){

			this.checkForm.medicine_forms.push({
					inspectName: "",
					key: Date.now(),
					});
		},
		removeCheck(oneCheck){

			var index = this.checkForm.medicine_forms.indexOf(oneCheck)
			if (index !== -1) {
			this.checkForm.medicine_forms.splice(index, 1)
			}
		},
		resetCheck(){

			this.checkForm.medicine_forms = [{inspectName:"",}]

		},
		fixCheckForm(){

			var nowDate = new Date();
			var nowDateFormated = nowDate.Format("yyyy-MM-dd");
			var oid = "2" + nowDate.Format("yyyyMMddhhmm") + this.loginUser.id + this.onePatient.id;

			this.checkForm.symptom = this.symptom;
			this.checkForm.diagnosis = this.diagnosis;
			this.checkForm.oid = oid;
			this.checkForm.type = 2;
			this.checkForm.registerLog = this.onePatient.id;
			this.checkForm.doctorId = this.loginUser.id;

			for (var i = 0; i < this.presForm.medicine_forms.length; i++){
				
				// 医嘱药物信息以外其他信息的补充
				this.checkForm.medicine_forms[i].startTime = nowDateFormated;
			};

		},
		confirmCheck(){

			this.fixCheckForm();
			this.showCheckFlag = true;
		},
		submitCheck(){

			this.showCheckFlag = false;
			addToPres(this.checkForm).then(resp => {
				if(resp.code == 0){
					
					this.$message({
						message: '检验单提交成功',
						type: 'success'
					});
					
					this.toDiagStep();
				}else{
					
					this.$message({
						message: resp.msg,
						type: 'warning'
					});
				};
			});
			
		},
		closeCheck(){

			this.showCheckFlag = false;
		},

		// 处方项目操作
		addPres(){

			this.presForm.medicine_forms.push({
					medicine: "",
					medication: "",
					period: "",
					freq: "",
					times: "",
					dose: "",
					allFreq: "",
					key: Date.now(),
					});

		},
		removePres(onePres){

			var index = this.presForm.medicine_forms.indexOf(onePres)
			if (index !== -1) {
			this.presForm.medicine_forms.splice(index, 1)
			}
		},
		resetPres(){

			this.presForm = {
				content:"",
				medicine_forms: [{
					medicine: "",
					medication: "",
					period: "",
					freq: "",
					times: "",
					dose: "",
					allFreq: "",
					},]
				};
		},

		// 提交处方
		addDate(date, days) {
			if (!days) {
			    days = 1;
			}
			var date = new Date(date);
			date.setDate(date.getDate() + days);
			return date;
		},

		fixPresForm(){

			var nowDate = new Date();
			var nowDateFormated = nowDate.Format("yyyy-MM-dd");
			var oid = "1" + nowDate.Format("yyyyMMddhhmm") + this.loginUser.id + this.onePatient.id;

			// 诊断信息添加到表内
			this.presForm.symptom = this.symptom;
			this.presForm.diagnosis = this.diagnosis;
			this.presForm.doctorId = this.loginUser.id;
			this.presForm.type = 1;
			this.presForm.registerLog = this.onePatient.id;
			this.presForm.oid = oid;

			for (var i = 0; i < this.presForm.medicine_forms.length; i++) {
				
				// 医嘱药物信息以外其他信息的补充
				this.presForm.medicine_forms[i].startTime = nowDateFormated;
				var endDate = this.addDate(nowDate, Number(this.presForm.medicine_forms[i].allFreq));
				var endDateFormated = endDate.Format("yyyy-MM-dd");
				this.presForm.medicine_forms[i].endTime = endDateFormated;
			};
		},
		confirmPres(){

			this.fixPresForm();
			this.showPresFlag = true;
			
		},
		submitPres(){

			
			addToPres(this.presForm).then(resp => {
				if(resp.code == 0){
					
					this.$message({
						message: '处方提交成功',
						type: 'success'
					});
					
					this.reloadQueue();
					this.showPresFlag = false;
				}else{
					
					this.$message({
						message: resp.msg,
						type: 'warning'
					});
				};
			});

		},
		closePres(){

			this.showPresFlag = false;
		},
		// 开具住院单
		sentHospital(){

			this.inHosLog.patientId = this.onePatient.patientId;
			this.inHosLog.status = 1;
			this.inHosLog.registerId = this.onePatient.id;
			this.inHosLog.token = this.$store.state.token;

			this.showSentHosFlag = true;
		},
		confirmSentHos(){

			sentToHos(this.inHosLog).then(resp => {
				if(resp.code == 0){
					
					this.$message({
						message: '住院单提交成功',
						type: 'success'
					});
					
					this.reloadQueue();
					this.showSentHosFlag = false;
				}else{
					
					this.$message({
						message: resp.msg,
						type: 'warning'
					});
				};
			});
			
		},
		closeSentHos(){

			this.showSentHosFlag = false;
		},
		// 刷新当前患者与患者队列
		reloadQueue(){

			this.tempId = {};
			this.tempId.id = this.onePatient.id;
			removeFromQueue(this.tempId);
			selectDoctorQueue(this.$store.state.token).then(resp =>{

				this.queueData = resp.data;
				if (this.queueData[0]) {

					this.onePatient = this.queueData[0];
				}else{

					this.onePatient = false;
				};
				this.symptom = "";
				this.resetCheck();
				this.diagnosis = "";
				this.resetPres();
				this.active = 0;
			});
		}

	},

	mounted(){

		getLoginUser(this.$store.state.token).then(resp => {

			this.loginUser = resp.data;
		});
		Date.prototype.Format = function(formatStr){ 
			var str = formatStr; 
			var Week = ['日','一','二','三','四','五','六']; 
			str=str.replace(/yyyy|YYYY/,this.getFullYear()); 
			str=str.replace(/yy|YY/,(this.getYear() % 100)>9?(this.getYear() % 100).toString():'0' + (this.getYear() % 100)); 
			
			var month = this.getMonth() + 1;
			if (this.getMonth()>9) {
				str=str.replace(/MM/, month.toString());
			} else {
				str=str.replace(/MM/, '0' + month.toString());
			};
			str=str.replace(/M/g, month);
			str=str.replace(/w|W/g,Week[this.getDay()]); 
			str=str.replace(/dd|DD/,this.getDate()>9?this.getDate().toString():'0' + this.getDate()); 
			str=str.replace(/d|D/g,this.getDate()); 
			str=str.replace(/hh|HH/,this.getHours()>9?this.getHours().toString():'0' + this.getHours()); 
			str=str.replace(/h|H/g,this.getHours()); 
			str=str.replace(/mm/,this.getMinutes()>9?this.getMinutes().toString():'0' + this.getMinutes()); 
			str=str.replace(/m/g,this.getMinutes()); 
			str=str.replace(/ss|SS/,this.getSeconds()>9?this.getSeconds().toString():'0' + this.getSeconds()); 
			str=str.replace(/s|S/g,this.getSeconds()); 
			return str;
			};
		

		// 后端还没实现就先注释掉，免得影响测试
		selectDoctorQueue(this.$store.state.token).then(resp =>{

			this.queueData = resp.data;
			if (this.queueData[0]) {

				this.onePatient = this.queueData[0];
			}else{

				this.onePatient = false;
			};
		});
	}
}
</script>