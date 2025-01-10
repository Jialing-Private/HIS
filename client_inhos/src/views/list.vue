<template>
    <div class="mybody">
		<el-card style="margin-bottom: 15px;" class="department-list">
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
						v-model="registForm.registerTime" :picker-options="DisableDatesOption"
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
</template>

<style>
</style>

<script>
import {
  addRegistes,
  getPageDoctors,
  getAllDepartments,
  getDoctorsByDept,
} from "../api";
export default {
    data() {
		
		let _this = this;
        return {
            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,

            departmentInfos: [],
            doctorOfOneDept: [],
            showDoctorFlag: false,

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
			DisableDatesOption: {
				disabledDate(time) {
					_this.resForm.setNowDate = _this.resForm.nowDate;
					let curDate = (new Date()).getTime();
					let pre = new Date();
					let oneDay = curDate - 24 * 3600 * 1000;
					let sevenDays = 7 * 24 * 3600 * 1000;
					let oneWeek = curDate + sevenDays;
					return time.getTime() < oneDay || time.getTime() > oneWeek;
				}
			},
        }
    },
    methods: {

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
				}else{
					
					this.$message({
						message: resp.msg,
						type: 'warning'
					});
				}
			});
		}
    },
    mounted(){

    	this.getDepartmentInfo();
    }
}
</script>
