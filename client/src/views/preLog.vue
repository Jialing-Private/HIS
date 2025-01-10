<template>
    <div>
	   	<el-card>
		    <div slot="header">
				<span class="el-icon-s-grid text-primary"></span> 今日预约
			</div>
		    <div>
				<el-row v-if="totalInfo > 0"  :gutter="15">
					<template v-for="item in pageInfos">
						<div v-if="item.queuePermission">
							<el-col :span="16">
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
							<el-col :span="8">
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
			:page-size="pageSize" layout="total, prev, pager, next" :total="totalInfo">
		</el-pagination>
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
	addToQueue
} from "../api";

export default {
    data() {

        return {
        	loginUser: {},
			statisInfo: {},
            pageInfos: [],
            pageIndex: 1,
            pageSize: 12,
            pageTotal: 0,
            totalInfo: 0,
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
            }
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {

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
        		}else{
        			this.$message.error('排队失败>_<')
        		};
				this.$router.push("/welcome");
        		
        	})
        }
		
    },
    mounted(){

    	getLoginUser(this.$store.state.token).then(resp =>{
			
			this.loginUser = resp.data;
		});
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});

        this.getPageInfo(1, this.pageSize);

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
    }
}
</script>
