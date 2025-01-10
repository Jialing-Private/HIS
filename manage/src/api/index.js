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
export function getAllNotices(){
	
	return http.get('/notices/all/');
}
export function getPageNotices(pageIndex, pageSize, title, value1, value2){

	return http.get('/notices/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, title: title, value1:value1, value2:value2}});
}
export function addNotices(params){
	
	return http.post('/notices/add/', params);
}
export function updNotices(params){
	
	return http.post('/notices/upd/', params);
}
export function delNotices(id){
	
	return http.post('/notices/del/', {id: id});
}

/** 科室信息接口 */
export function getAllDepartments(){

	return http.get('/departments/all/');
}
export function getInHosDepartments(){
	
	return http.get('/departments/inhos/');
}
export function getPageDepartments(pageIndex, pageSize, did, name, status){

	return http.get('/departments/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, did: did, name: name, status: status}});
}
export function addDepartments(params){
	
	return http.post('/departments/add/', params);
}
export function updDepartments(params){
	
	return http.post('/departments/upd/', params);
}
export function delDepartments(id){
	
	return http.post('/departments/del/', {id: id});
}
export function exportDepartments(did, name, status){
	
	return http.get('/departments/export/', {params: {did: did, name: name, status: status}});
}

/** 管理员信息接口 */
export function getPageManagers(pageIndex, pageSize, name, phone, gender, status, type1){
	
	return http.get('/managers/page/',
	{params: {pageIndex: pageIndex, pageSize: pageSize, name: name, phone: phone, gender: gender, status: status, type1: type1}});
}
export function exportManagers(name, phone, gender, status, type1){
	
	return http.get('/managers/export/',
	{params: {name: name, phone: phone, gender: gender, status: status, type1: type1}});
}
export function addManagers(params){
	
	return http.post('/managers/add/', params);
}
export function updManagers(params){
	
	return http.post('/managers/upd/', params);
}
export function delManagers(id){
	
	return http.post('/managers/del/', {id: id});
}

/** 医师信息接口 */
export function getPageDoctors(pageIndex, pageSize, name, phone, gender, education, job, registerFeeGte, registerFeeLte, departmentId, status){

	return http.get('/doctors/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name, phone: phone, 
		education: education, job: job, registerFeeGte: registerFeeGte, registerFeeLte: 
		registerFeeLte, gender: gender, departmentId: departmentId, status: status}});
}
export function exportDoctors(name, phone, gender, education, job, registerFeeGte, registerFeeLte, departmentId, status){

	return http.get('/doctors/export/', 
        {params: {name: name, phone: phone, 
		education: education, job: job, registerFeeGte: registerFeeGte, registerFeeLte: 
		registerFeeLte, gender: gender, departmentId: departmentId, status: status}});
}
export function addDoctors(params){
	
	return http.post('/doctors/add/', params);
}
export function updDoctors(params){
	
	return http.post('/doctors/upd/', params);
}
export function delDoctors(id){
	
	return http.post('/doctors/del/', {id: id});
}

/** 患者信息接口 */
export function getPagePatients(pageIndex, pageSize, name, phone, address, status, gender){

	return http.get('/patients/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name, phone: phone, address: address, status: status, gender: gender}});
}
export function exportPatients(name, phone, address, status, gender){

	return http.get('/patients/export/', 
        {params: {name: name, phone: phone, address: address, status: status, gender: gender}});
}
export function addPatients(params){
	
	return http.post('/patients/add/', params);
}
export function updPatients(params){
	
	return http.post('/patients/upd/', params);
}
export function delPatients(id){
	
	return http.post('/patients/del/', {id: id});
}

// 药品信息接口
export function getPageMedicine(pageIndex, pageSize, drugName, commonName, type, inventory1, inventory2, price1, price2){
	return http.get('/medicine/page/',
	    {params: {pageIndex: pageIndex, pageSize: pageSize, drugName: drugName, commonName: commonName, type: type,
		inventory1: inventory1, inventory2: inventory2, price1: price1, price2: price2}});
}

export function exportMedicine(drugName, commonName, type, inventory1, inventory2, price1, price2){
	return http.get('/medicine/export/',
	    {params: {drugName: drugName, commonName: commonName, type: type,
		inventory1: inventory1, inventory2: inventory2, price1: price1, price2: price2}});
}

export function addMedicine(params){
	
	return http.post('/medicine/add/', params);
}
export function updMedicine(params){
	
	return http.post('/medicine/upd/', params);
}
export function delMedicine(id){
	
	return http.post('/medicine/del/', {id: id});
}

// 入库单管理接口
export function getPageInWare(pageIndex, pageSize, drugName, commonName, type, date1, date2, inwareId, producer, handler, recorder){
	return http.get('/inware/page/',
	    {params: {pageIndex: pageIndex, pageSize: pageSize, drugName: drugName, commonName: commonName, type: type,
		date1: date1, date2: date2, inwareId: inwareId, producer: producer, handler: handler, recorder: recorder}});
}

export function exportInWare(drugName, commonName, type, date1, date2, inwareId, producer, handler, recorder){
	return http.get('/inware/export/',
	    {params: {drugName: drugName, commonName: commonName, type: type,
		date1: date1, date2: date2, inwareId: inwareId, producer: producer, handler: handler, recorder: recorder}});
}

export function addInWare(params){
	
	return http.post('/inware/add/', params);
}
export function delInWare(params){
	
	return http.post('/inware/del/', params);
}


/** 预约记录接口 */
export function getPageRegistes(pageIndex, pageSize, token, 
doctorName, patientName, value1, value2, departmentId){

	return http.get('/registes/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, token: token, doctorName: doctorName, patientName: patientName,
		value1: value1, value2: value2, departmentId: departmentId}});
}
export function exportRegistes(token, 
doctorName, patientName, value1, value2, departmentId){
	
	return http.get('/registes/export/', 
        {params: {token: token, doctorName: doctorName, patientName: patientName,
		value1: value1, value2: value2, departmentId: departmentId}});
}
export function addRegistes(params){
	
	return http.post('/registes/add/', params);
}
export function updRegistes(params){
	
	return http.post('/registes/upd/', params);
}
export function delRegistes(id){
	
	return http.post('/registes/del/', {id: id});
}

/** 床位信息接口 */
export function getPageBeds(pageIndex, pageSize, bid, pricegte, pricelte, type, status, departmentId){
	
	return http.get('/beds/page/', {params: {pageIndex: pageIndex, pageSize: pageSize, bid: bid, 
	pricegte: pricegte, pricelte: pricelte, 
	type: type, status: status, departmentId: departmentId}});
}
export function exportBeds(bid, pricegte, pricelte, type, status, departmentId){
	return http.get('/beds/export/', {params: {bid: bid,
	pricegte: pricegte, pricelte: pricelte, 
	type: type, status: status, departmentId: departmentId}});
}
export function addBeds(params){
	
	return http.post('/beds/add/', params);
}
export function updBeds(params){
	
	return http.post('/beds/upd/', params);
}
export function delBeds(id){
	
	return http.post('/beds/del/', {id: id});
}

/** 住院记录接口 */
export function getPageHospitalizationLogs(pageIndex, pageSize, token, doctorName,
 patientName, departmentId, startTime1, 
 startTime2, endTime1, endTime2, bedBid, status){
	
	return http.get('/inhospital/page/',
	{params: {pageIndex: pageIndex, pageSize: pageSize, token: token, doctorName: doctorName, patientName: patientName, departmentId: departmentId,
	startTime1: startTime1, startTime2: startTime2, endTime1: endTime1, endTime2: endTime2, bedBid: bedBid, status: status}});
}
export function exportHospitalizationLogs(token, doctorName,
patientName, departmentId, startTime1, 
startTime2, endTime1, endTime2, bedBid, status){
	
	return http.get('/inhospital/export/',
	{params: {token: token, doctorName: doctorName, patientName: patientName, departmentId: departmentId,
	startTime1: startTime1, startTime2: startTime2, endTime1: endTime1, endTime2: endTime2, bedBid: bedBid, status: status}});
}
export function addHospitalizationLogs(params){
	
	return http.post('/inhospital/add/', params);
}
export function updHospitalizationLogs(params){
	
	return http.post('/inhospital/upd/', params);
}
export function delHospitalizationLogs(id){
	
	return http.post('/inhospital/del/', {id: id});
}