<template>
	<div class = "mybody">
		<div class="regi-service-today">
			<div v-show="totalInfo">
				<el-card style="margin-bottom: 15px;">
					<div slot="header">
						<span class="el-icon-s-grid"></span> 今日预约
					</div>
					<div>
						<el-row v-if="totalInfo > 0"  :gutter="15">
							<template v-for="item in pageInfos">
								<div v-if="item.queuePermission">
									<el-col :span="8">
										<div class="register-panel">
											<div class="register-icon">
												<span class="el-icon-tickets"></span>
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
									<el-col :span="4">
										<div v-if="item.status == 0">
											<div class="preLog-button">
												<el-button :plain="true" @click="startQueue(item)" type="success">开始排队</el-button>
											</div>
										</div>
										<div v-else>
											<div class="preLog-button">
												<el-button :plain="true">已排队</el-button>
											</div>
										</div>
			   						</el-col>
			   					</div>
							</template>
						</el-row>
						<el-empty v-else description="暂无相关记录"></el-empty>
					</div>
				</el-card>
					<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="pageIndex"
					:page-size="pageSize" layout="total, prev, pager, next" 
					:total="totalInfo">
			</el-pagination>
			</div>

			<div>
				<el-card style="margin-bottom: 15px;">
					<div slot="header">
						<span class="el-icon-s-grid"></span> 科室列表
					</div>
					<div>
					   <el-row v-loading="loading" 
							element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
							element-loading-background="rgba(124, 124, 124, 0.8)" :gutter="15">
					   		<template v-for="item in departmentInfos">
					   			<el-col :span="8">
					   				<div @click="showDoctorWin(item.id)"  class="dept-panle">
					   					<div class="dept-img"></div>
					   					<div class="dept-info">
					   						<div class="doctor-info-item">
					   							<span class="dept-info-name">{{ item.name }}</span>
					   							<span class="dept-info-did">{{ item.did }}</span>
					   						</div>
					   					</div>
					   					<div class="dept-info-intro-panle">
					   						<div class="dept-info-intro">介绍: {{ item.describe }}</div>
					   					</div>
					   					
					   				</div>
					   			</el-col>
					   		</template>
					   	</el-row>
					</div>
				</el-card>

				<el-dialog title="医师列表" width="1000px" :visible.sync="showDoctorFlag">
					<div>
					   	<el-row v-loading="loading" 
							element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
							element-loading-background="rgba(124, 124, 124, 0.8)" :gutter="15">
					   		<template v-for="item in doctorOfOneDept">
					   			<el-col :span="8">
					   				<div @click="showRegisteWin(item)"  class="doctor-panle">
					   					<div class="doctor-img"></div>
					   					<div class="doctor-info">
					   						<div class="doctor-info-item">
					   							<span class="doctor-info-name">{{ item.name }}</span>
					   							<span class="doctor-info-title">{{ item.job }}</span>
					   							
					   						</div>
					   						<div class="doctor-info-good">
					   							擅长: {{ item.speciality }}
					   						</div>
					   					</div>
					   				</div>
					   			</el-col>
					   		</template>
					   	</el-row>
				   	</div>
				</el-dialog>
				
				<el-dialog title="挂号预约" width="600px" :visible.sync="showRegistFlag">
					<el-form label-width="90px" :model="registForm">
						<el-form-item label="挂号费用">
							<el-input v-model="registForm.registerFee" disabled></el-input>
						</el-form-item>
						<el-form-item label="预约时间">
							<el-date-picker style="width: 100%;"
								v-model="registForm.registerTime"
								:picker-options="DisableDatesOption"
								type="date" value-format="yyyy-MM-dd" placeholder="选择具体时间">
							</el-date-picker>
						</el-form-item>
					</el-form>
					<div slot="footer" class="dialog-footer">
						<el-button @click="showRegistFlag = false">取 消</el-button>
						<el-button type="primary" @click="addInfo()">确 定</el-button>
					</div>
				</el-dialog>
			</div>

			
		</div>

	</div>
    
</template>

<style>
</style>

<script>

import {
	getStatis,
	getPageRegistes,
	getLoginUser,
	updLoginUserInfo,
	addToQueue,
	addRegistes,
  	getPageDoctors,
  	getAllDepartments,
  	getDoctorsByDept,
} from "../api";

export default {
    data() {
		let _this = this;

        return {
        	loginUser: {},
			statisInfo: {},

            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,

            departmentInfos: [],
            doctorOfOneDept: [],

            showUpdUserFlag: false,
            queuePermission: true,
            userFrom: {
				card: '',
                address: '',
                userName: '',
                passWord: '',
                name: '',
                gender: '',
                age: '',
                phone: '',
                type: 2
            },
			
           
            loading: true,
			registForm: {
				token: this.$store.state.token,
				registerTime: '',
				registerFee: 0,
				status: 0,
				doctorId: '',
			},
			resForm: {
				nowDate: "",
				setNowDate: "",
			},
			showRegistFlag: false,
			showDoctorFlag: false,
			DisableDatesOption: {
				disabledDate(time) {
					_this.resForm.setNowDate = _this.resForm.nowDate;
					let curDate = (new Date()).getTime();
					let pre = new Date();
					let oneDay = 24 * 3600 * 1000;
					let sevenDays = 7 * 24 * 3600 * 1000;
					let oneWeek = curDate + sevenDays;
					return time.getTime() < (Date.now()-oneDay) || time.getTime() > oneWeek;
				}
			},


			showRepoFlag: false,
        	showPresFlag: false,
        	loginUser: {},
			statisInfo: {},
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

			presFrom: {
				medicine:'',
				dose:'',
				freq:'',
				patient: '',
                age: '',
                doctor: '',
                content: '',
                fee: '',
                department: '',
                time: '',
            },
        }
    },
    methods: {

        getPageInfoRegistes(pageIndex, pageSize) {

            getPageRegistes(pageIndex, pageSize, this.$store.state.token).then(resp => {

                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;

                var date = new Date();
                var Time = date.Format("yyyy-MM-dd");
                for (var i = 0; i < this.pageInfos.length; i++) {
                	if (this.pageInfos[i].registerTime == Time) {
                		this.pageInfos[i].queuePermission = true;
						
                	}else{
                		this.pageInfos[i].queuePermission = false;
                	};
					
                }

                this.loading = false;
            });
        },

        handleSizeChange(pageSize){

            this.getPageInfo(1, pageSize);
        },
        handleCurrentChange(pageIndex){

            this.getPageInfo(pageIndex, this.pageSize);
        },
        startQueue(item){

        	addToQueue(item).then(resp => {

        		if (resp.code == 0) {
        			this.$message({
	        			message: '排队成功^_^',
	        			type: 'success'
	        		});
	        		this.getPageInfoRegistes(this.pageIndex, this.pageSize);
        		}else{
        			this.$message.error('排队失败>_<')
        		};
				
        	})
        },


        getDepartmentInfo() {

            getAllDepartments().then(resp => {

                this.departmentInfos = resp.data;

                this.loading = false;
            });
        },
        showDoctorWin(deptId){

        	getDoctorsByDept(deptId).then(resp => {

        		this.doctorOfOneDept = resp.data;

        		this.showDoctorFlag = true;
        	})

        },
		showRegisteWin(info){
			
			if(this.registForm.token){
				
				this.registForm.registerFee = info.registerFee;
				this.registForm.doctorId = info.id;
				
				this.showRegistFlag = true;
			}else{
				
				this.$message({
					message: '未登陆用户无法进行预约',
					type: 'warning'
				});
			}
		},
		addInfo(){
			
			addRegistes(this.registForm).then(resp =>{
				
				if(resp.code == 0){
					
					this.$message({
						message: '预约成功, 请准时就医',
						type: 'success'
					});
					
					this.showRegistFlag = false;
					this.getPageInfoRegistes(this.pageIndex, this.pageSize);
				}else{
					
					this.$message({
						message: resp.msg,
						type: 'warning'
					});
				}
			});
		},

    },
    mounted(){

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

    	getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});

        
		this.getDepartmentInfo();
		this.getPageInfoRegistes(this.pageIndex, this.pageSize);

    }
}
</script>
