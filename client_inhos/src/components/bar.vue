<template>
    <div>
        <el-card style="margin-bottom:15px">
            <div slot="header">
			   <span class="fa fa-random text-primary"></span> 预约流程
			</div>
            <div style="height: 220px;">
				<el-steps direction="vertical">
				    <el-step status="finish" icon="el-icon-caret-bottom" title="步骤 1" description="新用户请先注册, 已有账号的直接登陆"></el-step>
				    <el-step status="finish" icon="el-icon-caret-bottom" title="步骤 2" description="浏览并选择合适的医师,点击页面预约按钮进行预约"></el-step>
				    <el-step status="finish" icon="el-icon-caret-bottom" title="步骤 3" description="预约记录在个人中心页面进行查看"></el-step>
				</el-steps>
			</div>
        </el-card>
         <el-card style="margin-bottom:15px">
            <div slot="header">
			   <span class="fa fa-bell text-primary"></span> 系统公告
			</div>
            <div> 
				为方便广大患者就医，节省挂号排队时间，本院提供并且推荐大家在线进行挂号预约，
				对于在线预约的患者本院将优先进行排号处理，感谢您的支持和配合，祝愿大家早日
				恢复健康！
			</div>
        </el-card>
    </div>
</template>

<style scoped>
.bar-comm{
    line-height: 25px;
    font-size: 14px;
    color: #606266;
    text-align: justify;
}
</style>

<script>

</script>
