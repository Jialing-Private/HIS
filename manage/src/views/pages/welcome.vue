<template>
    <div class="fater-body-show">
		<div class="fater-welcome">您好，欢迎使用不卜庐医院信息系统，祝您工作愉快</div>
        <el-row :gutter="15">
			<el-col :span="5">
				<el-card shadow="never">
					<div slot="header">
						科室总数
					</div>
					<div class="fater-num-panel">
						<div class="fater-num">{{ statisInfo.departmentTotal }}</div>
						<div class="fater-unit">个</div>
					</div>
				</el-card>
				<el-card style="margin-top: 15px;" shadow="never">
					<div slot="header">
						医师总数
					</div>
					<div class="fater-num-panel">
						<div class="fater-num">{{ statisInfo.doctorTotal }}</div>
						<div class="fater-unit">位</div>
					</div>
				</el-card>
			</el-col>
			<el-col :span="5">
			<el-card shadow="never">
				<div slot="header">
					今日入院人数
				</div>
				<div class="fater-num-panel">
					<div class="fater-num">{{ statisInfo.inHospitalTotal }}</div>
				</div>
			</el-card>
			<el-card style="margin-top: 15px;" shadow="never">
				<div slot="header">
					今日出院人数
				</div>
				<div class="fater-num-panel">
					<div class="fater-num">{{ statisInfo.outHospitalTotal }}</div>
					<div class="fater-unit">位</div>
				</div>
			</el-card>
			</el-col>
			<el-col :span="5">
			<el-card shadow="never">
				<div slot="header">
					今日挂号数
				</div>
				<div class="fater-num-panel">
					<div class="fater-num">{{ statisInfo.registerTotal }}</div>
				</div>
			</el-card>
			<el-card style="margin-top: 15px;" shadow="never">
				<div slot="header">
					今日就诊人数
				</div>
				<div class="fater-num-panel">
					<div class="fater-num">{{ statisInfo.jiuzhen }}</div>
					<div class="fater-unit">位</div>
				</div>
			</el-card>
			</el-col>
			<el-col :span="9">
							<el-card shadow="never">
								<div slot="header">系统信息</div>
								<div>
									<el-descriptions :column="1" border>
										<el-descriptions-item>
											<template slot="label">
												系统名称
											</template>
											不卜庐医院信息系统 V1.0.0
										</el-descriptions-item>
										<el-descriptions-item>
											<template slot="label">
												开发时间
											</template>
											2022-06-13
										</el-descriptions-item>
										<el-descriptions-item>
											<template slot="label">
												系统实现
											</template>
											Django + VUE + ElementUI + axios
										</el-descriptions-item>
										<el-descriptions-item>
											<template slot="label">
												运行环境
											</template>
											Python3.9 + MySQL8.x + NodeJS
										</el-descriptions-item>
										<el-descriptions-item>
											<template slot="label">
												开发工具
											</template>
											PyCharm + Hubilderx + Visual Studio Code
										</el-descriptions-item>
									</el-descriptions>
								</div>
							</el-card>
						</el-col>
		</el-row>
		<el-row :gutter="15">
			<el-col :span="8">
				<el-card shadow="never">
					<div slot="header">通知信息</div>
					<div>
						<el-timeline>
							<el-timeline-item color="#E6A23C" 
									v-for="(item, index) in notices" :key="index" 
									:timestamp="item.createTime" placement="top">
								<el-card>
									<div>
										{{item.content}}
									</div>
								</el-card>
							</el-timeline-item>
						</el-timeline>
					</div>
				</el-card>
			</el-col>
			<el-col :span="16">
				<el-card shadow="never">
					<div class="welcome-img"></div>
				</el-card>
			</el-col>
		</el-row>
    </div>
</template>

<script>
import {
	getStatis,
	getTopNotices
} from "../../api";
export default {
    data(){

        return {
			statisInfo: {},
			notices: []
        }
    },
    methods: {

    },
    mounted(){
		
		getStatis().then(resp =>{
			
			this.statisInfo = resp.data;
		});

        getTopNotices().then(resp => {

			this.notices = resp.data;
		});
    }
}

</script>

<style>
	.fater-welcome {
		padding: 5px 10px;
		height: 40px;
		line-height: 40px;
		background-color: #fff;
		margin-bottom: 15px;
		border-radius: 4px;
		border-left: 7px solid #009966;
	}

	.welcome-desc {
		line-height: 26px;
		text-align: justify;
		font-size: 14px;
		color: #606266;
	}

	.welcome-img {
		width: 100%;
		height: 500px;
		background-repeat: no-repeat;
		background-size: cover;
		background-image: url(../../assets/index.jpeg);
	}
</style>
