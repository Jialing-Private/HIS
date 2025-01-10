<template>
    <div>
        <div class="fater-welcome-panel"></div>
		<el-card style="margin-bottom: 15px;">
		    <div slot="header">
				<span class="el-icon-menu text-primary"></span>
				医师列表
			</div>
		    <div>
				<el-row v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :gutter="15">
					<template v-for="item in pageInfos">
						<el-col :span="8">
							<div  @click="showRegisteWin(item)" class="doctor-panle">
								<div class="doctor-img"></div>
								<div class="doctor-info">
									<div class="doctor-info-item">
										<span class="doctor-info-name">{{ item.name }}</span>
										<span class="doctor-info-title">{{ item.job }}</span>
										<span class="doctor-info-title">{{ item.officeName }}</span>
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
		</el-card>
		<el-dialog title="挂号预约" width="600px" :visible.sync="showRegisteFlag">
					<el-form label-width="90px" :model="registeForm">
						<el-form-item label="挂号费用">
							<el-input v-model="registeForm.total" disabled
								placeholder="请输入挂号费用…" autocomplete="off"></el-input>
						</el-form-item>
						<el-form-item label="预约时间">
							<el-date-picker style="width: 100%;"
							      v-model="registeForm.registeTime"
							      type="date" value-format="yyyy-MM-dd" placeholder="选择具体时间">
							</el-date-picker>
						</el-form-item>
					</el-form>
					<div slot="footer" class="dialog-footer">
						<el-button @click="showRegisteFlag = false">取 消</el-button>
						<el-button type="primary" @click="addInfo()">确 定</el-button>
					</div>
		</el-dialog>
    </div>
</template>

<script>
import {
    addRegistes,
    getPageDoctors
} from "../api";
export default {

    data(){

        return{
            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
			registeForm: {
				token: this.$store.state.token,
				registeTime: '',
				total: 0,
				status: 0,
				doctorId: '',
			},
			showRegisteFlag: false,
        }
    },
    methods: {
        
        getPageInfo(pageIndex, pageSize) {

            getPageDoctors(pageIndex, pageSize).then(resp => {

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
		showRegisteWin(info){
			
			if(this.registeForm.token){
				
				this.registeForm.total = info.registerFee;
				this.registeForm.doctorId = info.id;
				
				this.showRegisteFlag = true;
			}else{
				
				this.$message({
					message: '未登陆用户无法进行预约',
					type: 'warning'
				});
			}
		},
		addInfo(){
			
			addRegistes(this.registeForm).then(resp =>{
				
				if(resp.code == 0){
					
					this.$message({
						message: '预约成功, 请准时就医',
						type: 'success'
					});
					
					this.showRegisteFlag = false;
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
		
        this.getPageInfo(1, this.pageSize);
    }
}
</script>
