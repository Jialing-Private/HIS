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

//注销账号
export function delPatientUserInfo(token){
	return http.post('/patients/del/', {token: token});
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

/** client端个人住院信息的接口 */

/** 获取当前用户的住院单详细信息
 * 注：传入的参数是userId，返回查询"状态为：待入院"的患者的住院信息data，若该患者没有住院记录返回空。
 * 同时返回flag值(true或false)
 * data结构如下：
 * hospitalizationForm: {
			patient_id: '',
			status:0,
			department_Name:'',
			doctorName:''
		},*/
export function getPageUserHospitalization(pageIndex, pageSize, token){

	return http.get('/inhospital/page/', {params: {pageIndex: pageIndex, pageSize: pageSize, token: token}});
}
/** 提交患者选择床位、入院时间后的住院表单
 * 提交的表单结构如下：状态被修改为2表示已入院
 * hospitalizationForm: {
				patient_id: '',
				create_time: '',

				start_time: '',
				end_time: '',

				status:2,
				bed_id:'',
				department_Name:'',
				doctorName:''
			},
 */
export function upcompleteInhospital(params){

	return http.post('/inhospital/upd/', params);
}

export function getAvailableBedsInfo(departmentId){
	return http.get('/inhospital/bed/', {params: {departmentId: departmentId}});
}
   
export function getMoneyInfo(token, Id){
	return http.get('inhospital/money/', {params: {token: token, Id: Id}});
}

export function upaddpatientmoney(params){
	return http.post('inhospital/addmoney/',params);
}	 

export function getPageMedicalInfos(pageIndex, pageSize, token, patientName, oid, type){
	return http.get('/inhospital/medical/', {params: {pageIndex: pageIndex, pageSize: pageSize, token: token, patientName: patientName, oid: oid, type: type}});
}

//提现
export function upminuspatientmoney(params){
	return http.post('/inhospital/delmoney/', params);
}

export function exportDealInfo(params){
	return http.post('/inhospital/exportdeal/', params);
}

//医师端
export function upMedicalAdvice(params){
	return http.post('/inhospital/addma/', params);
}

//出院
export function upOuthospital(params){
	return http.post('/inhospital/out/', params);
}



/** 排队就诊（分诊）接口 */
export function addToQueue(params){

	return http.post('/queue/add/', params);
}
// 新增查询医生当前排队患者信息功能
export function selectDoctorQueue(token){

	return http.get('/queue/select/', {params: {token: token}});
}
// 新增修改预约记录status字段，完成诊疗过程功能
export function removeFromQueue(params){

	return http.post('/queue/remove/', params);
}


/** 检验报告接口 */
export function getPageRepos(pageIndex, pageSize, token){

	return http.get('/reports/page/',
		{params:{pageIndex: pageIndex, pageSize: pageSize, token: token}});
}

export function getDealInfo(pageIndex, pageSize, token){
 
	return http.get('/inhospital/deal/', {params: {pageIndex: pageIndex, pageSize: pageSize, token: token}});
}

/** 电子处方接口 */
export function getPagePreses(pageIndex, pageSize, token){

	return http.get('/prescripts/page/',
		{params:{pageIndex: pageIndex, pageSize: pageSize, token: token}});
}
// 新增添加门诊处方功能
export function addToPres(presForm){

	return http.post('/inhospital/addma/', presForm);
}
// 查询检验报告
export function getPresInfo(params){
	
	return http.post('/prescripts/info/', params);
}

/** 住院记录接口 */
export function sentToHos(inHosLog){

	return http.post('/inhospital/add/', inHosLog);
}


/** 科室信息接口 */
// 获取所有科室
export function getAllDepartments(){

	return http.get('/departments/all/');
}