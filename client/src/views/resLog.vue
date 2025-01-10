<template>
	<div>
	    <div>
		   	<el-card>
			    <div slot="header">
					<span class="el-icon-s-grid text-primary"></span> 检验报告
				</div>
			    <div>
					<el-row v-if="repoTotalInfo > 0"  :gutter="15">
						<template v-for="item in repoInfos">
							<el-col :span="8">
								<div class="register-panel">
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
								
								<div class="preLog-button">
									<el-button  @click="readRepo()" type="success">查看报告</el-button>
								</div>
								

	   						</el-col>
						</template>
					</el-row>
					<el-empty v-else description="暂无相关记录"></el-empty>
				</div>
			</el-card>
			<el-dialog title="检验报告" width="1100px" :visible.sync="showRepoFlag">
		    	<div class="report-img"></div>
		    	<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="closeRepo()">关 闭</el-button>
				</div> 
		    </el-dialog>
			<el-pagination v-if="repoPageTotal > 1" style="margin-top: 15px;" @size-change="handleRepoSizeChange"
				@current-change="handleRepoCurrentChange" :current-page="repoPageIndex"
				:page-size="repoPageSize" layout="total, prev, pager, next" :total="repoTotalInfo">
			</el-pagination>
	    </div>
	    <div>
		   	<el-card>
			    <div slot="header">
					<span class="el-icon-s-grid text-primary"></span> 历史处方
				</div>
			    <div>
					<el-row v-if="presTotalInfo > 0"  :gutter="15">
						<template v-for="item in presInfos">
							
								<el-col :span="8">
									<div class="register-panel">
										<div class="register-icon">
											<span class="el-icon-tickets"></span>
										</div>
										<div class="register-title">
											<span class="register-doctor-name">{{ item.doctorNamm }}</span>
											<span class="register-doctor-desc">{{ item.doctorJob }}</span>
											<span class="register-doctor-desc">{{ item.doctorOfficeName }}</span>
										</div>
										<div class="register-detail">
											<span class="register-detail-item">制定时间：{{ item.presTime }}</span>
										</div>
									</div>
								</el-col>
								<el-col :span="4">
									
										<div class="preLog-button">
											<el-button  @click="readPres(item)" type="success">查看处方</el-button>
										</div>
									
		   						</el-col>
		   					
						</template>
					</el-row>
					<el-empty v-else description="暂无相关记录"></el-empty>
				</div>
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
			<el-pagination v-if="presPageTotal > 1" style="margin-top: 15px;" @size-change="handlePresSizeChange"
				@current-change="handlePresCurrentChange" :current-page="presPageIndex"
				:page-size="presPageSize" layout="total, prev, pager, next" :total="presTotalInfo">
			</el-pagination>
	    </div>
	</div>
</template>

<style>
</style>

<script>

import {
	getStatis,
	getPagePreses,
	getLoginUser,
	getPageRepos,
	getPresInfo,
} from "../api";

export default {
    data() {

        return {
        	showRepoFlag: false,
        	showPresFlag: false,
        	loading: true,
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

			medicalAdvice:{},
			MedicineInfos:[],
            
        }
    },
    methods: {

    	// 获取检验报告页面信息
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
        }
		
    },
    mounted(){

    	getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});

        this.getRepoPageInfo(1, this.repoPageSize);
        this.getPresPageInfo(1, this.presPageSize);
    }
}
</script>
