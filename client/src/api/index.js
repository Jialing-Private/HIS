import http from "../utils/http.js";

/** 系统接口 */
export function getStatis(token){
	
	return http.get('/statis/');
}
export function login(param){
	
	return http.post('/login/', param);
}
export function exit(token){
	
	return http.get('/exit/', {params: token});
}
export function getLoginUser(token){
	
	return http.get('/info/', {params: {token: token}});
}
export function checkUserPwd(token, oldPwd){
	
	return http.get('/checkPwd/', {params: {token: token, oldPwd: oldPwd}});
}
export function updLoginUserInfo(params){
	
	return http.post('/info/', params);
}
export function updLoginUserPwd(token, newPwd){
	
	return http.post('/pwd/', {token: token, newPwd: newPwd});
}

/** 通知信息接口 */
export function getTopNotices(){

	return http.get('/notices/top/');
}

/** 医师信息接口 */
export function getPageDoctors(pageIndex, pageSize){

	return http.get('/doctors/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize}});
}
// 新增查找一个科室下所有医生信息的功能
export function getDoctorsByDept(deptId){

	return http.post('/doctors/select/', {deptId: deptId})
}

/** 患者信息接口 */
export function addPatients(params){
	
	return http.post('/patients/add/', params);
}

/** 预约记录接口 */
export function getPageRegistes(pageIndex, pageSize, token){

	return http.get('/registes/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, token: token}});
}
export function addRegistes(params){
	
	return http.post('/registes/add/', params);
}
export function updRegistes(params){
	
	return http.post('/registes/upd/', params);
}

/** 排队就诊（分诊）接口 */
export function addToQueue(params){

	return http.post('/queue/add/', params)
}
// 新增查询医生当前排队患者信息功能
export function selectDoctorQueue(token){

	return http.get('/queue/select/', {params: {token: token}})
}
// 新增修改预约记录status字段，完成诊疗过程功能
export function removeFromQueue(params){

	return http.post('/queue/remove/', params)
}


/** 检验报告接口 */
export function getPageRepos(pageIndex, pageSize, token){

	return http.get('/reports/page/',
		{params:{pageIndex: pageIndex, pageSize: pageSize, token: token}})
}



/** 电子处方接口 */
export function getPagePreses(pageIndex, pageSize, token){

	return http.get('/prescripts/page/',
		{params:{pageIndex: pageIndex, pageSize: pageSize, token: token}})
}
// 新增添加门诊处方功能
export function addToPres(presForm){

	return http.post('/inhospital/addma/', presForm)
}
/** 住院记录接口 */
export function sentToHos(inHosLog){

	return http.post('/inhospital/add/', inHosLog)
}


// 查询检验报告
export function getPresInfo(params){
	
	return http.post('/prescripts/info/',params)
}

/** 科室信息接口 */
// 获取所有科室
export function getAllDepartments(){

	return http.get('/departments/all/');
}