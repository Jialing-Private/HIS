from django.db import models


# 通知信息
class Notices(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    title = models.CharField('通知标题', max_length=32, null=False)
    content = models.CharField('通知内容', max_length=256, null=False)
    createTime = models.DateTimeField('通知发布时间', auto_now_add=True, db_column='create_time', null=False)
    updateTime = models.DateTimeField('通知更新时间', null=True)

    class Meta:
        db_table = 'notices'


# 用户信息
class Users(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    createTime = models.DateTimeField('添加时间', auto_now_add=True, db_column='create_time', null=False)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)
    # 0：管理员 1：医师 2：患者 3：药库管理员
    type = models.IntegerField('用户身份', null=False)

    class Meta:
        db_table = 'users'


# 科室信息
class Departments(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    did = models.CharField('科室号', max_length=10, unique=True)
    name = models.CharField('科室名', max_length=32, null=False, unique=True)
    describe = models.CharField('科室描述', max_length=256, null=False)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)
    status = models.IntegerField('科室状态', null=False)
    createTime = models.DateTimeField('创建时间', db_column='create_time', null=False, auto_now_add=True)

    class Meta:
        db_table = 'departments'


# 医师信息
class Doctors(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.SET_NULL, db_column='user_id', null=True)
    name = models.CharField('医师姓名', max_length=10, null=False)
    gender = models.CharField('医师性别', max_length=2, null=False)
    age = models.IntegerField('医师年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=100, null=True)
    education = models.CharField('医师学历', max_length=32, null=False)
    job = models.CharField('医师职称', max_length=20, null=False)
    speciality = models.CharField('专长描述', max_length=256, null=False)
    registerFee = models.FloatField('挂号费用', null=False)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, db_column='did', null=True)
    status = models.IntegerField('医师状态', null=False)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)
    createTime = models.DateTimeField('创建时间', db_column='create_time', null=False, auto_now_add=True)
    idNumber = models.CharField('身份证号', max_length=18, db_column='id_number', null=False, unique=True)

    class Meta:
        db_table = 'doctors'


# 管理员信息
class Managers(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.SET_NULL, db_column='user_id', null=True)
    name = models.CharField('管理员姓名', max_length=10, null=False)
    gender = models.CharField('管理员性别', max_length=2, null=False)
    age = models.IntegerField('管理员年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=100, null=True)
    type = models.CharField('管理员类型', max_length=6, null=True)
    status = models.IntegerField('管理员状态', null=False)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)
    createTime = models.DateTimeField('创建时间', db_column='create_time', null=False, auto_now_add=True)
    idNumber = models.CharField('身份证号', max_length=18, db_column='id_number', null=False, unique=True)

    class Meta:
        db_table = 'managers'


# 患者信息
class Patients(models.Model):
    id = models.AutoField('病人编号', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, db_column="userId", null=True)
    name = models.CharField('用户姓名', max_length=10, null=False)
    gender = models.CharField('用户性别', max_length=2, null=False)
    age = models.IntegerField('用户年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=100, null=True)
    idNumber = models.CharField('身份证号', max_length=18, db_column='id_number', null=False, unique=True)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)
    createTime = models.DateTimeField('创建时间', db_column='create_time', null=False, auto_now_add=True)
    status = models.IntegerField('病人账号状态', null=False)

    class Meta:
        db_table = 'patients'


# 挂号记录
class RegisterLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    registerTime = models.DateField('预约时间', db_column='register_time')
    createTime = models.DateTimeField('提交时间', db_column='create_time', auto_now_add=True, null=False)
    registerFee = models.FloatField('挂号费用', null=False)
    department = models.ForeignKey(Departments, null=True, on_delete=models.RESTRICT)
    # 0是挂号没排队，1是正在排队，2是就诊结束
    status = models.IntegerField('挂号状态', null=False)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctors, on_delete=models.RESTRICT, db_column='doctor_id')
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)

    class Meta:
        db_table = 'register_logs'


# 床位信息
class Beds(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    bid = models.CharField('床位编号', max_length=6, null=False, unique=True)
    price = models.FloatField('床位价格', null=False)
    type = models.CharField('床位类型', max_length=10, null=True)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField('床位状态', null=False)
    createTime = models.DateTimeField('创建时间', db_column='create_time', null=False, auto_now_add=True)
    updateTime = models.DateTimeField('最后更新时间', db_column='update_time', null=True)

    class Meta:
        db_table = 'beds'


# 住院记录
class HospitalizationLogs(models.Model):
    id = models.AutoField('住院编号', primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.RESTRICT, null=False)
    doctor = models.ForeignKey(Doctors, on_delete=models.RESTRICT, null=False)
    bed = models.ForeignKey(Beds, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Departments, on_delete=models.RESTRICT, null=False)
    createTime = models.DateTimeField('提交时间', db_column='create_time', auto_now_add=True, null=False)
    hospitalizationStartTime = models.DateField('入院日期', db_column='start_time', null=True)
    updateTime = models.DateTimeField('更新时间', db_column='update_time', null=True)
    hospitalizationEndTime = models.DateField('出院日期', db_column='end_time', null=True)
    duringTime = models.IntegerField('住院天数', db_column='during_time', null=True)
    # 3待出院，1待入院，2已入院，0已出院/患者拒绝入院
    status = models.IntegerField('患者状态', null=False)
    register = models.ForeignKey(RegisterLogs, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'hospitalization_logs'


# 药品信息
class Medicine(models.Model):
    id = models.AutoField('编号', primary_key=True)
    drugName = models.CharField('药品名', max_length=50, db_column="drug_name", null=True)
    commonName = models.CharField('通用名', max_length=50, unique=True, db_column="common_name",  null=False)
    unit = models.CharField('单位', max_length=6, null=True)
    price = models.FloatField('单价', null=False)
    inventory = models.IntegerField('库存', null=False, default=0)
    # 停用药/停产药，药物，检验
    type = models.CharField('类型', max_length=20, null=False)

    class Meta:
        db_table = 'medicine'


# 入库单表
class Inware(models.Model):
    id = models.AutoField('编号', primary_key=True)
    inwareId = models.CharField('入库单号', max_length=12, unique=True, db_column='inware_id', null=False)
    producer = models.CharField('供应商', max_length=12, null=False)
    inwareTime = models.DateField('入库日期', auto_now_add=True, null=False, db_column='inware_time')
    price = models.FloatField('合计总价', null=True)
    # 记录员，目前只有超级管理员或药库管理员可以记录
    recorder = models.ForeignKey(Managers, null=False, on_delete=models.RESTRICT)
    # 经手人，因为没有设计员工表这里不填
    handler = models.CharField('经手人', max_length=10, null=True)

    class Meta:
        db_table = 'inware'


# 入库单明细表
class InwareDetail(models.Model):
    id = models.AutoField('编号', primary_key=True)
    inware = models.ForeignKey(Inware, on_delete=models.CASCADE)
    # inwareId+序号就是明细号
    inwareDetailId = models.CharField('明细号', unique=True, max_length=14, null=False, db_column='inware_detail_id')
    price = models.FloatField('单价', null=False)
    plusPrice = models.FloatField('总价', null=False)
    num = models.IntegerField('数量', null=False)
    unit = models.CharField('单位', max_length=6, null=True)
    drugName = models.CharField('药品学名', max_length=50, null=True)
    commonName = models.CharField('药品通用名', max_length=50, null=False)
    type = models.CharField('类型', max_length=20, null=False)
    remarks = models.CharField('备注', max_length=255, null=True)

    class Meta:
        db_table = 'inware_detail'


# 检验项目表（新增）
class Inspection(models.Model):
    id = models.AutoField('检验项目编号', primary_key=True)
    name = models.CharField('检验项目名称', max_length=50, null=False)
    content = models.CharField('检验内容', max_length=255, null=False)
    price = models.FloatField('价格', null=False)
    # type列是指项目是否弃用的。分为正常/停用(主要是担心项目弃用是删除可能会导致医嘱中的数据级联删除或置空，
    # 相比用禁止删除不如设置type直接转为停用项目)
    type = models.CharField('类型', max_length=20, null=False)
    # 检验时间单位为小时
    inspectTime = models.FloatField('检验时间', null=False, db_column='inspect_time')

    class Meta:
        db_table = 'inspection'


# 医嘱（较大变动）
class MedicalAdvice(models.Model):
    id = models.AutoField('编号', primary_key=True)
    # 项目的单号（医嘱、门诊都是这个，可以在单号中加某个数字区分是哪种）
    oid = models.CharField('单号', max_length=16, null=False, unique=False)
    # 医嘱内容，门诊部分也可以用做附注或其他说明，看情况用
    content = models.CharField('内容', max_length=255, null=True)
    # 1: 门诊取药单 2:门诊检验单 3: 住院药物医嘱 4: 住院检验医嘱
    type = models.IntegerField('医嘱类型', null=False)
    # 住院医嘱需要填下面一个，是指住院单
    inHospitalLog = models.ForeignKey(HospitalizationLogs, db_column="inhospital_log", on_delete=models.CASCADE,
                                      null=True)
    # 门诊的话需要填下面三个，分别是门诊挂号单、开药医师、开药时间（也可以看情况将endDoctor和endTime作为药剂师和取药时间）
    registerLog = models.ForeignKey(RegisterLogs, db_column="register_log", on_delete=models.CASCADE, null=True)
    startTime = models.DateTimeField('起始时间', db_column="start_time", null=False)
    startDoctor = models.ForeignKey(Doctors, related_name="sDoctor", db_column="start_doctor",
                                    on_delete=models.RESTRICT, null=False)
    symptom = models.CharField('病情症状', null=True, max_length=500)
    diagnosis = models.CharField('诊断结果', null=True, max_length=500)
    # 门诊取药单的下边两个不用填，检验类的这两个是指检验医师、检验时间
    endDoctor = models.ForeignKey(Doctors, related_name="eDoctor", db_column="end_doctor", on_delete=models.RESTRICT,
                                  null=True)
    endTime = models.DateTimeField('结束时间', db_column="end_time", null=True)
    # 下边的是检验结果预计时间和出结果时间（报告时间），普通医嘱不用填
    inspectPreTime = models.DateTimeField('报告预计时间', db_column="inspect_pre_time", null=True)
    inspectTime = models.DateTimeField('报告时间', db_column="inspect_time", null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.RESTRICT, null=True)
    # 以下一项为检验项目，类别不是检验类不需要填
    inspection = models.ForeignKey(Inspection, on_delete=models.RESTRICT, null=True)
    # 检验类项目时可以作为检验次数等
    dose = models.IntegerField('用药量', null=True, default=1)
    # 用药频率以天为单位，如1天3次，2天（freq）1次（dose）等
    freq = models.IntegerField('用药频率', null=True, default=1)
    # 每个用药频率用药次数（一天三次指freq=1,times=3,dose是每次用药量,allFreq是用药时长，比如给三天的药，一天三次，一次dose的量）
    times = models.IntegerField('用药次数', null=True, default=1)
    allFreq = models.FloatField('用药总时长', null=True, db_column='all_freq')
    # 药品给药方式：常用的给药方法有涂抹、含化、填塞、雾化、灌肠、口服、注射与灌注等
    medication = models.CharField('给药方法', null=True, max_length=20)
    # 执行时将自动将药品表价格*dose*times*allFreq/freq自动输入price总价
    price = models.FloatField('总价', null=True)
    # 各种单据的创建时间
    createTime = models.DateTimeField('医嘱创建时间', null=True, db_column='create_time')

    class Meta:
        db_table = 'medical_advice'


# 电子钱包 不加病人，之后在后端确定是否是患者账号，确保账户余额为空时可以级联删除，否则不能删除。（不用patient是因为patient表不删除信息只置空user）
class EWallet(models.Model):
    id = models.AutoField('编号', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    balance = models.FloatField('余额', null=False)

    class Meta:
        db_table = 'e-wallet'


# 记录住院中的交易明细，包括住院医嘱和床位，医嘱按单计算，床位按天计算
class Dealing(models.Model):
    id = models.AutoField('编号', primary_key=True)
    eWallet = models.ForeignKey(EWallet, db_column='e-wallet', null=True, on_delete=models.SET_NULL)
    price = models.FloatField('交易费用', null=False)
    bedPrice = models.FloatField('床位费', null=True, db_column='bed_price')
    # 交易类型有三类：消费、充值、提现
    type = models.CharField('交易类型', null=False, max_length=6)
    dealTime = models.DateTimeField('交易时间', null=True, auto_now_add=True)
    medicalAdvice = models.ForeignKey(MedicalAdvice, null=True, on_delete=models.CASCADE, db_column='medical_advice')
    inHospitalLog = models.ForeignKey(HospitalizationLogs, null=True, on_delete=models.CASCADE,
                                      db_column="inhospital_log")
    paymethod = models.CharField('支付方式', max_length=20, null=True)

    class Meta:
        db_table = 'dealing'
