import json
import uuid
import datetime
import csv
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.views import View
import pandas as pd
from app import models
from itertools import chain


# 基础处理类
class BaseView(View):
    def isExist(param):
        if (param is None) or (param == ''):
            return False
        else:
            return True

    def parsePage(pageIndex, pageSize, pageTotal, count, data):
        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    def warnData(data, msg='状态异常'):
        resl = {'code': 1, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    def error(msg='系统异常'):
        resl = {'code': 2, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


# 解决'TypeError: Object of type ‘datetime’ is not JSON serializable'报错
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 系统处理
class SysView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return SysView.getSessionInfo(request)
        elif module == 'checkPwd':
            return SysView.checkPwd(request)
        elif module == 'exit':
            return SysView.exit(request)
        elif module == 'statis':
            return SysView.getStatis(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'info':
            return SysView.updSessionInfo(request)
        elif module == 'pwd':
            return SysView.updSessionPwd(request)
        elif module == 'login':
            return SysView.login(request)
        else:
            return BaseView.error()

    def getStatis(request):
        query = Q() & ~Q(status=0)
        a = models.Departments.objects.filter(query).count()
        b = models.Doctors.objects.filter(query).count()
        query = Q() & ~Q(status=0)
        query = query & Q(registerTime=datetime.datetime.now().strftime("%Y-%m-%d"))
        c = models.RegisterLogs.objects.filter(query).count()
        query = Q() & Q(hospitalizationStartTime=datetime.datetime.now().strftime("%Y-%m-%d"))
        d = models.HospitalizationLogs.objects.filter(query).count()
        query = Q() & Q(hospitalizationEndTime=datetime.datetime.now().strftime("%Y-%m-%d"))
        e = models.HospitalizationLogs.objects.filter(query).count()
        query = Q() & Q(status=2) & Q(registerTime=datetime.datetime.now().strftime("%Y-%m-%d"))
        f = models.RegisterLogs.objects.filter(query).count()
        resl = {
            'departmentTotal': a,
            'doctorTotal': b,
            'registerTotal': c,
            'inHospitalTotal': d,
            'outHospitalTotal': e,
            'jiuzhen': f,
        }
        return BaseView.successData(resl)

    def login(request):
        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')
        flag = int(request.POST.get('flag'))

        user = models.Users.objects.filter(userName=userName)

        if user.exists():
            data = list(user)
            if len(data) == 1:
                user = user.first()
                if (flag == 0) and (user.type == 2):
                    return SysView.warn('普通用户无权使用管理功能')
                elif (flag == 1) and (user.type == 0):
                    return SysView.warn('管理员无法登陆')
                elif (flag == 1) and (user.type == 3):
                    return SysView.warn('库存管理员无法登陆')
                else:
                    if user.passWord == passWord:
                        token = uuid.uuid4()
                        resl = {
                            'token': str(token),
                            'type': str(user.type),
                        }
                        cache.set(token, user.id, 60 * 60 * 60 * 3)
                        return SysView.successData(resl)
                    else:
                        return SysView.error('用户密码输入错误')
            elif len(data) == 2:
                b = []
                for item in data:
                    b.append(int(item.type))
                if 0 in b:
                    c = b.index(0)
                elif 1 in b:
                    c = b.index(1)
                user = data[c]
                if (flag == 0) and (user.type == 2):
                    return SysView.warn('普通用户无权使用管理功能')
                elif flag == 1:
                    if 2 in b:
                        cc = b.index(2)
                        user = data[cc]
                    if user.type == 0:
                        return SysView.warn('管理员无法登陆')
                    if user.type == 3:
                        return SysView.warn("库存管理员无法登陆")
                    else:
                        if user.passWord == passWord:
                            token = uuid.uuid4()
                            resl = {
                                'token': str(token),
                                'type': str(user.type),
                            }
                            cache.set(token, user.id, 60 * 60 * 60 * 3)
                            return SysView.successData(resl)
                        else:
                            return SysView.error('用户密码输入错误')
                else:
                    if user.passWord == passWord:
                        token = uuid.uuid4()
                        resl = {
                            'token': str(token),
                            'type': str(user.type),
                        }
                        cache.set(token, user.id, 60 * 60 * 60 * 3)
                        return SysView.successData(resl)
                    else:
                        return SysView.error('用户密码输入错误')
        else:
            return SysView.error('用户名输入错误')

    def getLoginUser(token):
        user = models.Users.objects.filter(id=cache.get(token)).first()
        resl = {
            'userId': user.id,
            'userName': user.userName,
            'passWord': user.passWord,
            'userCreateTime': datetime.datetime.strftime(user.createTime, "%Y-%m-%d %H:%M:%S"),
            'type': user.type,
        }
        if BaseView.isExist(user.updateTime):
            resl['userUpdateTime'] = datetime.datetime.strftime(user.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['userUpdateTime'] = ''
        if int(user.type) == 0 or int(user.type) == 3:
            if models.Managers.objects.filter(user__id=user.id).exists():
                data = models.Managers.objects.filter(user__id=user.id).first()
                a = int(data.status)
                if a == 1:
                    b = '正常'
                elif a == 2:
                    b = '请假'
                elif a == 0:
                    b = '离职'
                resl['id'] = data.id
                resl['name'] = data.name
                resl['gender'] = data.gender
                resl['age'] = data.age
                resl['phone'] = data.phone
                resl['address'] = data.address
                resl['status'] = b
                resl['createTime'] = datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S")
                resl['idNumber'] = data.idNumber
                resl['type1'] = data.type
                if BaseView.isExist(data.updateTime):
                    resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    resl['updateTime'] = ''
        elif int(user.type) == 1:
            if models.Doctors.objects.filter(user__id=user.id).exists():
                data = models.Doctors.objects.filter(user__id=user.id).first()
                a = int(data.status)
                if a == 1:
                    b = '正常'
                elif a == 2:
                    b = '请假'
                elif a == 0:
                    b = '离职'
                resl['id'] = data.id
                resl['idNumber'] = data.idNumber
                resl['name'] = data.name
                resl['education'] = data.education
                resl['gender'] = data.gender
                resl['age'] = data.age
                resl['phone'] = data.phone
                resl['address'] = data.address
                resl['status'] = b
                resl['speciality'] = data.speciality
                resl['createTime'] = datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S")
                if BaseView.isExist(data.updateTime):
                    resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    resl['updateTime'] = ''
        elif int(user.type) == 2:
            if models.Patients.objects.filter(user__id=user.id).exists():
                data = models.Patients.objects.filter(user__id=user.id).first()
                a = int(data.status)
                if a == 1:
                    b = '正常'
                elif a == 0:
                    b = '账号已注销'
                resl['id'] = data.id
                resl['name'] = data.name
                resl['gender'] = data.gender
                resl['age'] = data.age
                resl['phone'] = data.phone
                resl['address'] = data.address
                resl['idNumber'] = data.idNumber
                resl['status'] = b
                resl['createTime'] = datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S")
                if BaseView.isExist(data.updateTime):
                    resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    resl['updateTime'] = ''
        return resl

    def exit(request):
        token = request.GET.get('token')
        cache.delete(token)
        return BaseView.success()

    def checkPwd(request):
        oldPwd = request.GET.get('oldPwd')
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        if loginUser['passWord'] == oldPwd:
            return BaseView.success()
        else:
            return BaseView.warn('原始密码输入错误')

    def getSessionInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        return BaseView.successData(loginUser)

    def updSessionInfo(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        if (request.POST.get('userName') != loginUser['userName']) & \
                (models.Users.objects.filter(userName=request.POST.get('userName')).exists()):
            c = list(models.Users.objects.filter(userName=request.POST.get('userName')))
            d = []
            for item in c:
                d.append(int(item.type))
            if loginUser['type'] == 0 or loginUser['type'] == 1 or loginUser['type'] == 3:
                if 0 in d or 1 in d or 3 in d:
                    return BaseView.warn('用户账号已存在无法重复添加')
            elif loginUser['type'] == 2:
                if 2 in d:
                    return BaseView.warn('用户账号已存在无法重复添加')
        if int(loginUser['type']) == 0 or loginUser['type'] == 3:
            a = request.POST.get('status')
            if a == '正常':
                b = 1
            elif a == '请假':
                b = 2
            elif a == '离职':
                b = 0
            models.Managers.objects.filter(
                user__id=loginUser['userId']
            ).update(
                name=request.POST.get('name'),
                age=request.POST.get('age'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                idNumber=request.POST.get('idNumber'),
                status=b,
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                type=request.POST.get('type'),
            )
        elif int(loginUser['type']) == 1:
            a = request.POST.get('status')
            if a == '正常':
                b = 1
            elif a == '请假':
                b = 2
            elif a == '离职':
                b = 0
            models.Doctors.objects.filter(
                user__id=loginUser['userId']
            ).update(
                name=request.POST.get('name'),
                age=request.POST.get('age'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                idNumber=request.POST.get('idNumber'),
                status=b,
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                speciality=request.POST.get('speciality'),
            )
        elif int(loginUser['type']) == 2:
            a = request.POST.get('status')
            if a == '正常':
                b = 1
            elif a == '账号已注销':
                b = 0
            models.Patients.objects.filter(
                user__id=loginUser['userId']
            ).update(
                name=request.POST.get('name'),
                age=request.POST.get('age'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                idNumber=request.POST.get('idNumber'),
                status=b,
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        models.Users.objects.filter(
            id=loginUser['userId']
        ).update(
            userName=request.POST.get('userName'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def updSessionPwd(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        models.Users.objects.filter(
            id=loginUser['userId']
        ).update(
            passWord=request.POST.get('newPwd'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()


# 通知信息处理
class NoticesView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return NoticesView.getInfo(request)
        elif module == 'top':
            return NoticesView.getTopList(request)
        elif module == 'page':
            return NoticesView.getPageInfo(request)
        elif module == 'all':
            return NoticesView.getAll(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return NoticesView.addInfo(request)
        elif module == 'upd':
            return NoticesView.updInfo(request)
        elif module == 'del':
            return NoticesView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Notices.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'title': data.title,
            'content': data.content,
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
        }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getAll(request):
        data = models.Notices.objects.all()
        resl = []
        for item in list(data):
            temp = {
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        return BaseView.successData(resl)

    def getTopList(request):
        resl = []
        notices = models.Notices.objects.all().order_by("-createTime")[:7]
        for item in list(notices):
            temp = {
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        title = request.GET.get('title')
        date1 = request.GET.get('value1')
        date2 = request.GET.get('value2')
        query = Q()
        if BaseView.isExist(title):
            query = query & Q(title__contains=title)
        if BaseView.isExist(date1):
            query = query & Q(createTime__gte=date1)
        if BaseView.isExist(date2):
            date2 = datetime.datetime.strftime(datetime.datetime.strptime(date2, "%Y-%m-%d") +
                                               datetime.timedelta(days=1), "%Y-%m-%d")
            query = query & Q(createTime__lte=date2)
        data = models.Notices.objects.filter(query).order_by('-createTime')
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def addInfo(request):
        models.Notices.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return BaseView.success()

    def updInfo(request):
        models.Notices.objects.filter(id=request.POST.get('id')).update(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return BaseView.success()

    def delInfo(request):
        models.Notices.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()


# 科室信息管理
class DepartmentsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return DepartmentsView.getInfo(request)
        elif module == 'all':
            return DepartmentsView.getAll(request)
        elif module == 'inhos':
            return DepartmentsView.getInHos(request)
        elif module == 'page':
            return DepartmentsView.getPageInfo(request)
        elif module == 'export':
            return DepartmentsView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return DepartmentsView.addInfo(request)
        elif module == 'upd':
            return DepartmentsView.updInfo(request)
        elif module == 'del':
            return DepartmentsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Departments.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'did': data.did,
            'name': data.name,
            'describe': data.describe,
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
            'status': data.status,
        }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getAll(request):
        data = models.Departments.objects.all()
        resl = []
        for item in list(data):
            temp = {
                'id': item.id,
                'did': item.did,
                'name': item.name,
                'describe': item.describe,
                'status': item.status,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        return BaseView.successData(resl)

    def getInHos(request):
        data = models.Departments.objects.filter(status=2)
        resl = []
        for item in list(data):
            temp = {
                'id': item.id,
                'did': item.did,
                'name': item.name,
                'describe': item.describe,
                'status': item.status,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        status = request.GET.get('status')
        did = request.GET.get('did')
        query = Q()
        if BaseView.isExist(status):
            query = query & Q(status=status)
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(did):
            query = query & Q(did=did)
        data = models.Departments.objects.filter(query).order_by("-did")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            if a == 0:
                b = '已停用'
            elif a == 1:
                b = '门诊部'
            elif a == 2:
                b = '住院部'
            elif a == 3:
                b = '其他'
            else:
                b = ''
            temp = {
                'id': item.id,
                'did': item.did,
                'name': item.name,
                'describe': item.describe,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status': b
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        name = request.GET.get('name')
        status = request.GET.get('status')
        did = request.GET.get('did')
        query = Q()
        if BaseView.isExist(status):
            query = query & Q(status=status)
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(did):
            query = query & Q(did=did)
        data = models.Departments.objects.filter(query).order_by("-did")
        resl = []
        for item in list(data):
            a = int(item.status)
            if a == 0:
                b = '已停用'
            elif a == 1:
                b = '门诊部'
            elif a == 2:
                b = '住院部'
            elif a == 3:
                b = '其他'
            else:
                b = ''
            temp = {
                'id': item.id,
                'did': item.did,
                'name': item.name,
                'describe': item.describe,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status2': b
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('科室列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                              ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    def addInfo(request):
        models.Departments.objects.create(
            did=request.POST.get('did'),
            name=request.POST.get('name'),
            describe=request.POST.get('describe'),
            status=request.POST.get('status'),
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def updInfo(request):
        models.Departments.objects.filter(
            id=request.POST.get('id')
        ).update(
            did=request.POST.get('did'),
            name=request.POST.get('name'),
            describe=request.POST.get('describe'),
            status=request.POST.get('status'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def delInfo(request):
        models.Departments.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()


# 药品管理
class MedicineView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return MedicineView.getInfo(request)
        elif module == 'page':
            return MedicineView.getPageInfo(request)
        elif module == 'export':
            return MedicineView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return MedicineView.addInfo(request)
        elif module == 'upd':
            return MedicineView.updInfo(request)
        elif module == 'del':
            return MedicineView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Medicine.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'drugName': data.name,
            'commonName': data.commonName,
            'unit': data.unit,
            'price': data.price,
            'inventory': data.inventory,
            'type': data.type,
        }
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        commonName = request.GET.get('commonName')
        name = request.GET.get('drugName')
        type1 = request.GET.get('type')
        inventory1 = request.GET.get('inventory1')
        inventory2 = request.GET.get('inventory2')
        price1 = request.GET.get('price1')
        price2 = request.GET.get('price2')
        query = Q()
        if BaseView.isExist(commonName):
            query = query & Q(commonName__contains=commonName)
        if BaseView.isExist(type1):
            query = query & Q(type__contains=type1)
        if BaseView.isExist(inventory2):
            query = query & Q(inventory__lte=inventory2)
        if BaseView.isExist(inventory1):
            query = query & Q(inventory__gte=inventory1)
        if BaseView.isExist(price1):
            query = query & Q(price__gte=price1)
        if BaseView.isExist(price2):
            query = query & Q(price__lte=price2)
        if BaseView.isExist(name):
            query = query & Q(drugName__contains=name)
        data = models.Medicine.objects.filter(query).order_by("id")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'drugName': item.drugName,
                'commonName': item.commonName,
                'unit': item.unit,
                'price': item.price,
                'inventory': item.inventory,
                'type': item.type,
            }
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        commonName = request.GET.get('commonName')
        name = request.GET.get('drugName')
        type1 = request.GET.get('type')
        inventory1 = request.GET.get('inventory1')
        inventory2 = request.GET.get('inventory2')
        price1 = request.GET.get('price1')
        price2 = request.GET.get('price2')
        query = Q()
        if BaseView.isExist(commonName):
            query = query & Q(commonName__contains=commonName)
        if BaseView.isExist(type1):
            query = query & Q(phone__contains=type1)
        if BaseView.isExist(inventory2):
            query = query & Q(inventory__lte=inventory2)
        if BaseView.isExist(inventory1):
            query = query & Q(inventory__gte=inventory1)
        if BaseView.isExist(price1):
            query = query & Q(price__gte=price1)
        if BaseView.isExist(price2):
            query = query & Q(price__lte=price2)
        if BaseView.isExist(name):
            query = query & Q(drugName__contains=name)
        data = models.Medicine.objects.filter(query).order_by("id")
        resl = []
        for item in list(data):
            temp = {
                'id': item.id,
                'drugName': item.drugName,
                'commonName': item.commonName,
                'unit': item.unit,
                'price': item.price,
                'inventory': item.inventory,
                'type': item.type,
            }
            resl.append(temp)
        if resl:
            with open('药品列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                               ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    @transaction.atomic
    def addInfo(request):
        commonName = request.POST.get('commonName')
        if models.Medicine.objects.filter(commonName=commonName).exists():
            return BaseView.error('已存在该药品')
        else:
            models.Medicine.objects.create(
               commonName=commonName,
               drugName=request.POST.get('drugName'),
               type=request.POST.get('type'),
               unit=request.POST.get('unit'),
               price=request.POST.get('price'),
               inventory=request.POST.get('inventory'),
            )
        return BaseView.success('添加成功')

    def updInfo(request):
        models.Medicine.objects.filter(
            id=request.POST.get('id')
        ).update(
            commonName=request.POST.get('commonName'),
            drugName=request.POST.get('drugName'),
            type=request.POST.get('type'),
            unit=request.POST.get('unit'),
            price=request.POST.get('price'),
            inventory=request.POST.get('inventory')
        )
        return BaseView.success('更新成功')

    @transaction.atomic
    def delInfo(request):
        models.Medicine.objects.filter(
            id=request.POST.get('id')
        ).update(
            type='停用药',
            inventory=0,
        )
        return BaseView.success('删除成功')


# 药品入库管理
class MedicineInWareView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return MedicineInWareView.getInfo(request)
        elif module == 'page':
            return MedicineInWareView.getPageInfo(request)
        elif module == 'export':
            return MedicineInWareView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return MedicineInWareView.addInfo(request)
        elif module == 'upd':
            return MedicineInWareView.updInfo(request)
        elif module == 'del':
            return MedicineInWareView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Medicine.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'inwareDetailId': data.inwareDetailId,
            'producer': data.inware.producer,
            'inwareId': data.inware.id,
            'inwareTime': datetime.datetime.strftime(data.inware.inwareTime, '%Y-%m-%d'),
            'plusPrice': data.plusPrice,
            'sumPrice': data.inware.price,
            'num': data.num,
            'drugName': data.drugName,
            'commonName': data.commonName,
            'type': data.type,
            'remarks': data.remarks,
            'unit': data.unit,
            'handler': data.inware.handler,
            'recorderId': data.inware.recorder.id,
            'recorderName': data.inware.recorder.name,
        }
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        commonName = request.GET.get('commonName')
        inwareId = request.GET.get('inwareId')
        name = request.GET.get('drugName')
        type1 = request.GET.get('type')
        producer = request.GET.get('producer')
        handler = request.GET.get('handler')
        recorder = request.GET.get('recorder')
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        query = Q()
        if BaseView.isExist(commonName):
            query = query & Q(commonName__contains=commonName)
        if BaseView.isExist(type1):
            query = query & Q(type__contains=type1)
        if BaseView.isExist(date2):
            query = query & Q(inware__inwareTime__lte=date2)
        if BaseView.isExist(date1):
            query = query & Q(inware__inwareTime__gte=date1)
        if BaseView.isExist(inwareId):
            query = query & Q(inware__inwareId__gte=inwareId)
        if BaseView.isExist(producer):
            query = query & Q(inware__producer__contains=producer)
        if BaseView.isExist(handler):
            query = query & Q(inware__handler__contains=handler)
        if BaseView.isExist(recorder):
            query = query & Q(inware__recorder__contains=recorder)
        if BaseView.isExist(name):
            query = query & Q(drugName__contains=name)
        if BaseView.isExist(inwareId):
            data = models.InwareDetail.objects.filter(query).or_by('id')
        else:
            data = models.InwareDetail.objects.filter(query).order_by("-inwareDetailId")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'inwareDetailId': item.inwareDetailId,
                'producer': item.inware.producer,
                'inwareId': item.inware.id,
                'inwareTime': datetime.datetime.strftime(item.inware.inwareTime, '%Y-%m-%d'),
                'plusPrice': item.plusPrice,
                'sumPrice': item.inware.price,
                'num': item.num,
                'drugName': item.drugName,
                'commonName': item.commonName,
                'type': item.type,
                'remarks': item.remarks,
                'price': item.price,
                'unit': item.unit,
                'handler': item.inware.handler,
                'recorderId': item.inware.recorder.id,
                'recorderName': item.inware.recorder.name,
                'recorderType': item.inware.recorder.type,
            }
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        commonName = request.GET.get('commonName')
        inwareId = request.GET.get('inwareId')
        name = request.GET.get('drugName')
        type1 = request.GET.get('type')
        producer = request.GET.get('producer')
        handler = request.GET.get('handler')
        recorder = request.GET.get('recorder')
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        query = Q()
        if BaseView.isExist(commonName):
            query = query & Q(commonName__contains=commonName)
        if BaseView.isExist(type1):
            query = query & Q(type__contains=type1)
        if BaseView.isExist(date2):
            query = query & Q(inware__inwareTime__lte=date2)
        if BaseView.isExist(date1):
            query = query & Q(inware__inwareTime__gte=date1)
        if BaseView.isExist(inwareId):
            query = query & Q(inware__inwareId__gte=inwareId)
        if BaseView.isExist(producer):
            query = query & Q(inware__producer__contains=producer)
        if BaseView.isExist(handler):
            query = query & Q(inware__handler__contains=handler)
        if BaseView.isExist(recorder):
            query = query & Q(inware__recorder__contains=recorder)
        if BaseView.isExist(name):
            query = query & Q(drugName__contains=name)
        if BaseView.isExist(inwareId):
            data = models.InwareDetail.objects.filter(query).or_by('id')
        else:
            data = models.InwareDetail.objects.filter(query).order_by("-inwareDetailId")
        resl = []
        for item in list(data):
            temp = {
                'id': item.id,
                'inwareDetailId': item.inwareDetailId,
                'producer': item.inware.producer,
                'inwareId': item.inware.id,
                'inwareTime': datetime.datetime.strftime(item.inware.inwareTime, '%Y-%m-%d'),
                'plusPrice': item.plusPrice,
                'sumPrice': item.inware.price,
                'num': item.num,
                'drugName': item.drugName,
                'commonName': item.commonName,
                'type': item.type,
                'remarks': item.remarks,
                'unit': item.unit,
                'handler': item.inware.handler,
                'recorderId': item.inware.recorder.id,
                'recorderName': item.inware.recorder.name,
                'recorderType': item.inware.recorder.type,
            }
            resl.append(temp)
        if resl:
            with open('入库单{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                               ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    @transaction.atomic
    def addInfo(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        inwareTime = request.POST.get('inwareTime')
        producer = request.POST.get('producer')
        handler = request.POST.get('handler')
        inwareId = request.POST.get('inwareId')
        priceList = request.POST.getlist('inWareDetail[price]')
        drugNameList = request.POST.getlist('inWareDetail[drugName]')
        commonNameList = request.POST.getlist('inWareDetail[commonName]')
        typeList = request.POST.getlist('inWareDetail[type]')
        remarksList = request.POST.getlist('inWareDetail[remarks]')
        unitList = request.POST.getlist('inWareDetail[unit]')
        numList = request.POST.getlist('inWareDetail[num]')
        aa = models.Inware.objects.create(
            inwareId=inwareId,
            producer=producer,
            inwareTime=datetime.datetime.strptime(inwareTime, '%Y-%m-%d'),
            recorder=models.Managers.objects.filter(id=loginUser['id']).first(),
            handler=handler,
        )
        sumPrice = 0
        for i in range(len(commonNameList)):
            models.InwareDetail.objects.create(
                inware=aa,
                inwareDetailId='{0}{1:02d}'.format(str(inwareId), i + 1),
                price=priceList[i],
                num=numList[i],
                plusPrice=int(numList[i]) * float(priceList[i]),
                unit=unitList[i],
                drugName=drugNameList[i],
                commonName=commonNameList[i],
                type=typeList[i],
                remarks=remarksList[i],
            )
            sumPrice += int(numList[i]) * float(priceList[i])
            a = models.Medicine.objects.filter(commonName=commonNameList[i])
            if a.exists():
                models.Medicine.objects.filter(commonName=commonNameList[i]).update(
                    inventory=int(a.first().inventory) + int(numList[i]),
                )
            else:
                models.Medicine.objects.create(
                    price=priceList[i],
                    inventory=numList[i],
                    unit=unitList[i],
                    drugName=drugNameList[i],
                    commonName=commonNameList[i],
                    type=typeList[i],
                )
        models.Inware.objects.filter(inwareId=inwareId).update(
            price=sumPrice
        )
        return BaseView.success('添加成功')

    def updInfo(request):
        return BaseView.success()

    @transaction.atomic
    def delInfo(request):
        type1 = int(request.POST.get('type'))
        if type1 == 2:
            a = models.InwareDetail.objects.filter(id=request.POST.get('id'))
            c = int(a.first().inware.id)
            data = models.InwareDetail.objects.filter(inware__id=c)
            for item in list(data):
                a = int(item.num)
                b = item.commonName
                d = int(models.Medicine.objects.filter(commonName=b).first().inventory)
                models.Medicine.objects.filter(commonName=b).update(
                    inventory=d - a,
                )
            models.Inware.objects.filter(id=c).delete()
        elif type1 == 1:
            c = int(models.InwareDetail.objects.filter(id=request.POST.get('id')).first().num)
            d = models.InwareDetail.objects.filter(id=request.POST.get('id')).first().commonName
            models.InwareDetail.objects.filter(id=request.POST.get('id')).delete()
            e = int(models.Medicine.objects.filter(commonName=d).first().inventory)
            models.Medicine.objects.filter(commonName=d).update(
                inventory=e - c,
            )
        else:
            return BaseView.error('删除失败')
        return BaseView.success('删除成功')


# 管理员信息管理
class ManagersView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return ManagersView.getInfo(request)
        elif module == 'page':
            return ManagersView.getPageInfo(request)
        elif module == 'export':
            return ManagersView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return ManagersView.addInfo(request)
        elif module == 'upd':
            return ManagersView.updInfo(request)
        elif module == 'del':
            return ManagersView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Managers.objects.filter(id=request.GET.get('id')).first()
        if int(data.status) != 0:
            resl = {
                'id': data.id,
                'userId': data.user.id,
                'userName': data.user.name,
                'userCreateTime': datetime.datetime.strftime(data.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'address': data.address,
                'status': data.status,
                'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
                'idNumber': data.idNumber,
                'type': data.type,
            }
        else:
            resl = {
                'id': data.id,
                'userId': '',
                'userName': '',
                'userCreateTime': datetime.datetime.strftime(data.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'address': data.address,
                'status': data.status,
                'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
                'idNumber': data.idNumber,
                'type': data.type,
            }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        gender = request.GET.get('gender')
        status = request.GET.get('status')
        type1 = request.GET.get('type1')
        query = Q()
        if status == '正常':
            b = 1
            query = query & Q(status=b)
        elif status == '请假':
            b = 2
            query = query & Q(status=b)
        elif status == '离职':
            b = 0
            query = query & Q(status=b)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(phone__contains=phone)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        if BaseView.isExist(type1):
            query = query & Q(type__contains=type1)
        data = models.Managers.objects.filter(query).order_by("-createTime")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            if a == 1:
                b = '正常'
            elif a == 2:
                b = '请假'
            elif a == 0:
                b = '离职'
                temp = {
                    'userId': '',
                    'userName': '',
                    'passWord': '',
                    'userCreateTime': '',
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'id': item.id,
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'address': item.address,
                    'status': b,
                    'idNumber': item.idNumber,
                    'type1': item.type,
                }
                if BaseView.isExist(item.updateTime):
                    temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    temp['updateTime'] = ''
                resl.append(temp)
                continue
            else:
                b = ''
            temp = {
                'userId': item.user.id,
                'userName': item.user.userName,
                'passWord': item.user.passWord,
                'type': item.user.type,
                'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'id': item.id,
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'address': item.address,
                'status': b,
                'idNumber': item.idNumber,
                'type1': item.type,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        gender = request.GET.get('gender')
        status = request.GET.get('status')
        type1 = request.GET.get('type1')
        query = Q()
        if status == '正常':
            b = 1
            query = query & Q(status=b)
        elif status == '请假':
            b = 2
            query = query & Q(status=b)
        elif status == '离职':
            b = 0
            query = query & Q(status=b)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(user__name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(user__phone__contains=phone)
        if BaseView.isExist(type1):
            query = query & Q(type__contains=type1)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        data = models.Managers.objects.filter(query).order_by("-createTime")
        resl = []
        for item in list(data):
            a = int(item.status)
            if a == 1:
                b = '正常'
            elif a == 2:
                b = '请假'
            elif a == 0:
                b = '离职'
                temp = {
                    'userId': '',
                    'userName': '',
                    'userCreateTime': '',
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'id': item.id,
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'address': item.address,
                    'status': b,
                    'idNumber': item.idNumber,
                    'type': item.type,
                }
                if BaseView.isExist(item.updateTime):
                    temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    temp['updateTime'] = ''
                resl.append(temp)
                continue
            else:
                b = ''
            temp = {
                'userId': item.user.id,
                'userName': item.user.userName,
                'type': item.type,
                'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'id': item.id,
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'address': item.address,
                'status': b,
                'idNumber': item.idNumber,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('管理员列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                               ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    @transaction.atomic
    def addInfo(request):
        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            a = list((models.Users.objects.filter(userName=request.POST.get('userName'))))
            b = []
            for item in a:
                b.append(int(item.type))
            if 0 in b or 1 in b:
                return BaseView.warn('该账号已存在，无法重复添加')
        if request.POST.get('type1') == '药库管理员':
            type1 = 3
        elif request.POST.get('type1') == '超级管理员':
            type1 = 0
        else:
            type1 = 0
        user = models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            type=type1,
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        c = request.POST.get('idNumber')
        if models.Managers.objects.filter(idNumber=c).exists():
            models.Managers.objects.filter(idNumber=c).update(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status=1,
                type=request.POST.get('type1')
            )
        else:
            models.Managers.objects.create(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status=1,
                idNumber=request.POST.get('idNumber'),
                type=request.POST.get('type1'),
            )
        return BaseView.success()

    def updInfo(request):
        a = request.POST.get('type1')
        c = models.Managers.objects.filter(id=request.POST.get('id')).first().user.id
        models.Managers.objects.filter(
            id=request.POST.get('id')
        ).update(
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            status=request.POST.get('status'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            idNumber=request.POST.get('idNumber'),
            type=a,
        )
        if a == '超级管理员':
            b = 0
        elif a == '药库管理员':
            b = 3
        else:
            b = 0
        models.Users.objects.filter(id=c).update(
            type=b
        )
        if int(request.POST.get('status')) == 0:
            a = models.Managers.objects.filter(id=request.POST.get('id')).first().user_id
            models.Users.objects.filter(a).delete()
        return BaseView.success()

    @transaction.atomic
    def delInfo(request):
        a = models.Managers.objects.filter(id=request.POST.get('id')).first().user_id
        models.Users.objects.filter(id=a).delete()
        models.Managers.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=0,
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()


# 医师信息管理
class DoctorsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return DoctorsView.getInfo(request)
        elif module == 'page':
            return DoctorsView.getPageInfo(request)
        elif module == 'export':
            return DoctorsView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return DoctorsView.addInfo(request)
        elif module == 'upd':
            return DoctorsView.updInfo(request)
        elif module == 'del':
            return DoctorsView.delInfo(request)
        elif module == 'select':
            return DoctorsView.selectByDept(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Doctors.objects.filter(id=request.GET.get('id')).first()
        if int(data.status) != 0:
            resl = {
                'id': data.id,
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'address': data.address,
                'education': data.education,
                'job': data.job,
                'speciality': data.speciality,
                'registerFee': data.registerFee,
                'status': data.status,
                'departmentId': data.department.id,
                'userId': data.user.id,
                'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
                'idNumber': data.idNumber,
            }
        else:
            resl = {
                'id': data.id,
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'address': data.address,
                'education': data.education,
                'job': data.job,
                'speciality': data.speciality,
                'registerFee': data.registerFee,
                'status': data.status,
                'departmentId': data.department.id,
                'userId': '',
                'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
                'idNumber': data.idNumber,
            }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        registerFeeGte = request.GET.get('registerFeeGte')
        registerFeeLte = request.GET.get('registerFeeLte')
        job = request.GET.get('job')
        departmentId = request.GET.get('departmentId')
        gender = request.GET.get('gender')
        education = request.GET.get('education')
        status = request.GET.get('status')
        query = Q()
        if status == '正常':
            b = 1
            query = query & Q(status=b)
        elif status == '请假':
            b = 2
            query = query & Q(status=b)
        elif status == '离职':
            b = 0
            query = query & Q(status=b)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(phone__contains=phone)
        if BaseView.isExist(registerFeeGte):
            query = query & Q(registerFee__gte=registerFeeGte)
        if BaseView.isExist(registerFeeLte):
            query = query & Q(registerFee__lte=registerFeeLte)
        if BaseView.isExist(job):
            query = query & Q(job__contains=job)
        if BaseView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        if BaseView.isExist(education):
            query = query & Q(education__contains=education)
        data = models.Doctors.objects.filter(query).order_by("-createTime")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            if BaseView.isExist(item.status):
                a = int(item.status)
                if a == 0:
                    b = '离职'
                    temp = {
                        'userId': '',
                        'userName': '',
                        'passWord': '',
                        'id': item.id,
                        'name': item.name,
                        'gender': item.gender,
                        'age': item.age,
                        'phone': item.phone,
                        'userCreateTime': '',
                        'type': '',
                        'education': item.education,
                        'job': item.job,
                        'speciality': item.speciality,
                        'registerFee': item.registerFee,
                        'departmentId': item.department.id,
                        'departmentIdentifier': item.department.did,
                        'departmentName': item.department.name,
                        'status': b,
                        'address': item.address,
                        'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                        'idNumber': item.idNumber,
                    }
                    if BaseView.isExist(item.updateTime):
                        temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                    else:
                        temp['updateTime'] = ''
                    resl.append(temp)
                    continue
                elif a == 1:
                    b = '正常'
                elif a == 2:
                    b = '请假'
                else:
                    b = ''
                temp = {
                    'userId': item.user.id,
                    'id': item.id,
                    'userName': item.user.userName,
                    'passWord': item.user.passWord,
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                    'type': item.user.type,
                    'education': item.education,
                    'job': item.job,
                    'speciality': item.speciality,
                    'registerFee': item.registerFee,
                    'departmentId': item.department.id,
                    'departmentIdentifier': item.department.did,
                    'departmentName': item.department.name,
                    'status': b,
                    'address': item.address,
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'idNumber': item.idNumber,
                }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        registerFeeGte = request.GET.get('registerFeeGte')
        registerFeeLte = request.GET.get('registerFeeLte')
        job = request.GET.get('job')
        departmentId = request.GET.get('departmentId')
        gender = request.GET.get('gender')
        education = request.GET.get('education')
        status = request.GET.get('status')
        query = Q()
        if status == '正常':
            b = 1
            query = query & Q(status=b)
        elif status == '请假':
            b = 2
            query = query & Q(status=b)
        elif status == '离职':
            b = 0
            query = query & Q(status=b)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(phone__contains=phone)
        if BaseView.isExist(registerFeeGte):
            query = query & Q(registerFee__gte=registerFeeGte)
        if BaseView.isExist(registerFeeLte):
            query = query & Q(registerFee__lte=registerFeeLte)
        if BaseView.isExist(job):
            query = query & Q(job__contains=job)
        if BaseView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        if BaseView.isExist(education):
            query = query & Q(education__contains=education)
        data = models.Doctors.objects.filter(query).order_by("-createTime")
        resl = []
        for item in list(data):
            a = int(item.status)
            if a == 1:
                b = '正常'
            elif a == 2:
                b = '请假'
            elif a == 0:
                b = '离职'
                temp = {
                    'userId': '',
                    'id': item.id,
                    'userName': '',
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'userCreateTime': '',
                    'education': item.education,
                    'job': item.job,
                    'speciality': item.speciality,
                    'registerFee': item.registerFee,
                    'departmentId': item.department.id,
                    'departmentDid': item.department.did,
                    'departmentName': item.department.name,
                    'status': b,
                    'address': item.address,
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'idNumber': item.idNumber,
                }
                if BaseView.isExist(item.updateTime):
                    temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    temp['updateTime'] = ''
                resl.append(temp)
                continue
            else:
                b = ''
            temp = {
                'userId': item.user.id,
                'id': item.id,
                'userName': item.user.userName,
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'education': item.education,
                'job': item.job,
                'speciality': item.speciality,
                'registerFee': item.registerFee,
                'departmentId': item.department.id,
                'departmentDid': item.department.did,
                'departmentName': item.department.name,
                'status': b,
                'address': item.address,
                'idNumber': item.idNumber,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('医师列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                              ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    @transaction.atomic
    def addInfo(request):
        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            a = list(models.Users.objects.filter(userName=request.POST.get('userName')))
            b = []
            for item in a:
                b.append(int(item.type))
            if 0 in b or 1 in b:
                return BaseView.warn('该账号已存在，无法重复添加')
        user = models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            type=request.POST.get('type'),
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        c = request.POST.get('idNumber')
        if models.Doctors.objects.filter(idNumber=c).exists():
            models.Doctors.objects.filter(idNumber=c).update(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                education=request.POST.get('education'),
                job=request.POST.get('job'),
                speciality=request.POST.get('speciality'),
                registerFee=request.POST.get('registerFee'),
                department=models.Departments.objects.get(id=request.POST.get('departmentId')),
                status=1,
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        else:
            models.Doctors.objects.create(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                education=request.POST.get('education'),
                job=request.POST.get('job'),
                speciality=request.POST.get('speciality'),
                registerFee=request.POST.get('registerFee'),
                department=models.Departments.objects.get(id=request.POST.get('departmentId')),
                status=1,
                createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                idNumber=request.POST.get('idNumber'),
            )
        return BaseView.success()

    def updInfo(request):
        models.Doctors.objects.filter(
            id=request.POST.get('id')
        ).update(
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            education=request.POST.get('education'),
            job=request.POST.get('job'),
            speciality=request.POST.get('speciality'),
            registerFee=request.POST.get('registerFee'),
            department=models.Departments.objects.get(id=request.POST.get('departmentId')),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            idNumber=request.POST.get('idNumber'),
        )
        a = request.POST.get('status')
        if BaseView.isExist(a):
            if a == '请假':
                b = 2
            elif a == '正常':
                b = 1
            elif a == '离职':
                b = 0
                a = models.Doctors.objects.filter(id=request.POST.get('id')).first().user_id
                models.Users.objects.filter(id=a).delete()
            models.Doctors.objects.filter(
                id=request.POST.get('id')
            ).update(
                status=b
            )
        return BaseView.success()

    @transaction.atomic
    def delInfo(request):
        a = models.Doctors.objects.filter(id=request.POST.get('id')).first().user_id
        models.Users.objects.filter(id=a).delete()
        models.Doctors.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=0,
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def selectByDept(request):
        resl = []
        doctorList = models.Doctors.objects.filter(department__id=request.POST.get('deptId'))
        for item in doctorList:
            if item.status == 1:
                temp = {
                    'userId': item.user.id,
                    'id': item.id,
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'education': item.education,
                    'job': item.job,
                    'speciality': item.speciality,
                    'registerFee': item.registerFee,
                }
                resl.append(temp)
        return BaseView.successData(resl)

# 患者信息管理
class PatientsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return PatientsView.getInfo(request)
        elif module == 'page':
            return PatientsView.getPageInfo(request)
        elif module == 'export':
            return PatientsView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return PatientsView.addInfo(request)
        elif module == 'upd':
            return PatientsView.updInfo(request)
        elif module == 'del':
            return PatientsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Patients.objects.filter(id=request.GET.get('id')).first()
        if int(data.status) != 0:
            resl = {
                'id': data.id,
                'address': data.address,
                'idNumber': data.idNumber,
                'userId': data.user.id,
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'status': data.status,
            }
        else:
            resl = {
                'id': data.id,
                'address': data.address,
                'idNumber': data.idNumber,
                'userId': '',
                'name': data.name,
                'gender': data.gender,
                'age': data.age,
                'phone': data.phone,
                'status': data.status,
            }
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        address = request.GET.get('address')
        gender = request.GET.get('gender')
        status = request.GET.get('status')
        query = Q()
        if status == '正常':
            query = query & Q(status=1)
        elif status == '账号已注销':
            query = query & Q(status=0)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(phone__contains=phone)
        if BaseView.isExist(address):
            query = query & Q(address__contains=address)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        data = models.Patients.objects.filter(query).order_by("-createTime")

        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            if a == 1:
                b = '正常'
            elif a == 0:
                b = '账号已注销'
                temp = {
                    'id': item.id,
                    'userId': '',
                    'userName': '',
                    'passWord': '',
                    'type': '',
                    'userCreateTime': '',
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'address': item.address,
                    'idNumber': item.idNumber,
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'status': b,
                }
                if BaseView.isExist(item.updateTime):
                    temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    temp['updateTime'] = ''
                resl.append(temp)
                continue
            else:
                b = ''
            temp = {
                'id': item.id,
                'userId': item.user.id,
                'userName': item.user.userName,
                'passWord': item.user.passWord,
                'type': item.user.type,
                'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'address': item.address,
                'idNumber': item.idNumber,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status': b,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        address = request.GET.get('address')
        gender = request.GET.get('gender')
        status = request.GET.get('status')
        query = Q()
        if status == '正常':
            query = query & Q(status=1)
        elif status == '账号已注销':
            query = query & Q(status=0)
        elif status == '不限':
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(name):
            query = query & Q(name__contains=name)
        if BaseView.isExist(phone):
            query = query & Q(phone__contains=phone)
        if BaseView.isExist(address):
            query = query & Q(address__contains=address)
        if BaseView.isExist(gender):
            if gender == '不限':
                pass
            else:
                query = query & Q(gender__contains=gender)
        data = models.Patients.objects.filter(query).order_by("-createTime")
        resl = []
        for item in list(data):
            a = int(item.status)
            if a == 1:
                b = '正常'
            elif a == 0:
                b = '账号已注销'
                temp = {
                    'id': item.id,
                    'userId': '',
                    'userName': '',
                    'type': '',
                    'userCreateTime': '',
                    'name': item.name,
                    'gender': item.gender,
                    'age': item.age,
                    'phone': item.phone,
                    'address': item.address,
                    'idNumber': item.idNumber,
                    'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'status': b,
                }
                if BaseView.isExist(item.updateTime):
                    temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
                else:
                    temp['updateTime'] = ''
                resl.append(temp)
                continue
            else:
                b = ''
            temp = {
                'id': item.id,
                'userId': item.user.id,
                'userName': item.user.userName,
                'type': item.user.type,
                'userCreateTime': datetime.datetime.strftime(item.user.createTime, "%Y-%m-%d %H:%M:%S"),
                'name': item.name,
                'gender': item.gender,
                'age': item.age,
                'phone': item.phone,
                'address': item.address,
                'idNumber': item.idNumber,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status': b,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('患者列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                              ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    @transaction.atomic
    def addInfo(request):
        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            a = list(models.Users.objects.filter(userName=request.POST.get('userName')))
            b = []
            for item in a:
                b.append(int(item.type))
            if 2 in b:
                return BaseView.warn('该账号已存在，无法重复添加')
        user = models.Users.objects.create(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            type=request.POST.get('type'),
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        c = request.POST.get('idNumber')
        if models.Patients.objects.filter(idNumber=c).exists():
            models.Patients.objects.filter(idNumber=c).update(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                idNumber=request.POST.get('idNumber'),
                createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status=1,
            )
        else:
            models.Patients.objects.create(
                user=user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                idNumber=request.POST.get('idNumber'),
                createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status=1,
            )
        models.EWallet.objects.create(
            user=user,
            balance=0,
        )
        return BaseView.success()

    def updInfo(request):
        models.Patients.objects.filter(
            id=request.POST.get('id')
        ).update(
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=request.POST.get('status'),
        )
        if int(request.POST.get('status')) == 0:
            a = models.Patients.objects.filter(id=request.POST.get('id')).first().user_id
            models.Users.objects.filter(id=a).delete()
        return BaseView.success()

    @transaction.atomic
    def delInfo(request):
        token = request.POST.get('token')
        if BaseView.isExist(request.POST.get('id')):
            if models.RegisterLogs.objects.filter(patient__id=request.POST.get('id')).exists():
                a = models.Patients.objects.filter(id=request.POST.get('id')).first().user_id
                models.Users.objects.filter(id=a).delete()
                models.Patients.objects.filter(
                    id=request.POST.get('id')
                ).update(
                    updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=0,
                )
            else:
                a = models.Patients.objects.filter(id=request.POST.get('id')).first().user_id
                models.Patients.objects.filter(id=request.POST.get('id')).delete()
                models.Users.objects.filter(id=a).delete()
        elif BaseView.isExist(token):
            loginUser = SysView.getLoginUser(request.POST.get('token'))
            if models.RegisterLogs.objects.filter(patient__id=loginUser['id']).exists():
                models.Users.objects.filter(id=loginUser['userId']).delete()
                models.Patients.objects.filter(
                    id=loginUser['id']
                ).update(
                    updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=0,
                )
            else:
                models.Patients.objects.filter(id=loginUser['id']).delete()
                models.Users.objects.filter(id=loginUser['userId']).delete()
        else:
            return BaseView.error('注销失败')
        return BaseView.success()


# 挂号记录管理
class RegisterLogsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return RegisterLogsView.getInfo(request)
        elif module == 'page':
            return RegisterLogsView.getPageInfo(request)
        elif module == 'export':
            return RegisterLogsView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return RegisterLogsView.addInfo(request)
        elif module == 'upd':
            return RegisterLogsView.updInfo(request)
        elif module == 'del':
            return RegisterLogsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.RegisterLogs.objects.filter(id=request.GET.get('id')).first()
        c = int(data.status)
        if c == 0:
            d = '未就诊'
        elif c == 1:
            d = '排队中'
        elif c == 2:
            d = '已就诊'
        else:
            d = ''
        resl = {
            'id': data.id,
            'registerTime': datetime.datetime.strftime(data.registerTime, "%Y-%m-%d"),
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
            'registerFee': data.registerFee,
            'patientId': data.patient.id,
            'doctorId': data.doctor.id,
            'status': d,
        }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        registerTime1 = request.GET.get('value1')
        registerTime2 = request.GET.get('value2')
        departmentId = request.GET.get('departmentId')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        if loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if BaseView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if BaseView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if BaseView.isExist(registerTime1):
            query = query & Q(registerTime__gte=registerTime1)
        if BaseView.isExist(registerTime2):
            registerTime2 = datetime.datetime.strftime(datetime.datetime.strptime(registerTime2, "%Y-%m-%d") +
                                                       datetime.timedelta(days=1), "%Y-%m-%d")
            query = query & Q(registerTime__lte=registerTime2)
        if BaseView.isExist(departmentId):
            query = query & (Q(doctor__department__id=departmentId) | Q(department__id=departmentId))
        data = models.RegisterLogs.objects.filter(query).order_by("-createTime")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            c = int(item.status)
            if c == 0:
                d = '未就诊'
            elif c == 2:
                d = '已就诊'
            elif c == 1:
                d = '排队中'
            else:
                d = ''
            temp = {
                'status2': d,
                'id': item.id,
                'registerTime': datetime.datetime.strftime(item.registerTime, "%Y-%m-%d"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerFee': item.registerFee,
                'status': item.status,
                'patientId': item.patient.id,
                'patientName': item.patient.name,
                'patientGender': item.patient.gender,
                'patientAge': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'doctorId': item.doctor.id,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorName': item.doctor.name,
                'doctorDepartmentId': item.doctor.department.id,
                'doctorDepartmentName': item.doctor.department.name,
                'departmentName': item.department.name,
                'departmentId': item.department.id,
                'departmentDid': item.department.did,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        registerTime1 = request.GET.get('value1')
        registerTime2 = request.GET.get('value2')
        departmentId = request.GET.get('departmentId')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        if loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if BaseView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if BaseView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if BaseView.isExist(registerTime1):
            query = query & Q(registerTime__gte=registerTime1)
        if BaseView.isExist(registerTime2):
            registerTime2 = datetime.datetime.strftime(datetime.datetime.strptime(registerTime2, "%Y-%m-%d") +
                                                       datetime.timedelta(days=1), "%Y-%m-%d")
            query = query & Q(registerTime__lte=registerTime2)
        if BaseView.isExist(departmentId):
            query = query & Q(doctor__department__id=departmentId)
        data = models.RegisterLogs.objects.filter(query).order_by("-createTime")
        resl = []
        for item in list(data):
            c = int(item.status)
            if c == 0:
                d = '未就诊'
            elif c == 2:
                d = '已就诊'
            elif c == 1:
                d = '排队中'
            else:
                d = ''
            temp = {
                'id': item.id,
                'registerTime': datetime.datetime.strftime(item.registerTime, "%Y-%m-%d"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerFee': item.registerFee,
                'status': d,
                'patientId': item.patient.id,
                'patientName': item.patient.name,
                'patientGender': item.patient.gender,
                'patientAge': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'doctorId': item.doctor.id,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorName': item.doctor.name,
                'doctorDepartmentId': item.doctor.department.id,
                'doctorDepartmentName': item.doctor.department.name,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('挂号信息列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                                ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    def addInfo(request):
        user = SysView.getLoginUser(request.POST.get('token'))

        query = Q()
        query = query & Q(patient__user__id=user['userId'])
        query = query & Q(doctor__id=request.POST.get('doctorId'))
        registerTime = request.POST.get('registerTime')
        if BaseView.isExist(registerTime):
            query = query & Q(registerTime=registerTime)
        elif BaseView.isExist(request.POST.get('registeTime')):
            registerTime = request.POST.get('registeTime')
            query = query & Q(registerTime=registerTime)
        else:
            registerTime = ''
        if models.RegisterLogs.objects.filter(query).exists():
            return BaseView.warn('预约记录已存在')
        else:
            if BaseView.isExist(registerTime):
                registerFee = request.POST.get('registerFee')
                if BaseView.isExist(registerFee):
                    pass
                elif BaseView.isExist(request.POST.get('total')):
                    registerFee = request.POST.get('total')
                else:
                    return BaseView.error('挂号费错误')
                models.RegisterLogs.objects.create(
                    registerFee=registerFee,
                    status=request.POST.get('status'),
                    registerTime=registerTime,
                    department=models.Doctors.objects.filter(id=request.POST.get('doctorId')).first().department,
                    createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    patient=models.Patients.objects.filter(user__id=user['userId']).first(),
                    doctor=models.Doctors.objects.filter(id=request.POST.get('doctorId')).first()
                )
            else:
                BaseView.error('预约时间错误')
            return BaseView.success()

    def updInfo(request):
        models.RegisterLogs.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=request.POST.get('status'),
        )
        return BaseView.success()

    def delInfo(request):
        models.RegisterLogs.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()


# 床位信息管理
class BedsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return BedsView.getInfo(request)
        elif module == 'page':
            return BedsView.getPageInfo(request)
        elif module == 'export':
            return BedsView.exportInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return BedsView.addInfo(request)
        elif module == 'upd':
            return BedsView.updInfo(request)
        elif module == 'del':
            return BedsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.Beds.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'bid': data.bid,
            'price': data.price,
            'type': data.type,
            'departmentId': data.department.id,
            'status': data.status,
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
        }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageInfo(request):
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        priceGte = request.GET.get('pricegte')
        priceLte = request.GET.get('pricelte')
        bid = request.GET.get('bid')
        departmentId = request.GET.get('departmentId')
        status = request.GET.get('status')
        type1 = request.GET.get('type')

        query = Q()

        if status == "停用":
            query = query & Q(status=0)
        elif status == "正常":
            query = query & Q(status=1)
        elif status == '使用中':
            query = query & Q(status=2)
        elif status == "占用中":
            query = query & Q(status=3)
        elif status == "查看全部":
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(priceLte):
            query = query & Q(price__lte=priceLte)
        if BaseView.isExist(priceGte):
            query = query & Q(price__gte=priceGte)
        if BaseView.isExist(bid):
            query = query & Q(bid__contains=bid)
        if BaseView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if BaseView.isExist(type1):
            if type1 == "查看全部":
                pass
            else:
                query = query & Q(type__contains=type1)
        data = models.Beds.objects.filter(query).order_by("id")

        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            b = ""
            if a == 0:
                b = "停用"
            elif a == 1:
                b = "正常"
            elif a == 2:
                b = "使用中"
            elif a == 3:
                b = "占用中"
            else:
                b = "其他"
            temp = {
                'id': item.id,
                'bid': item.bid,
                'price': item.price,
                'type': item.type,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status': b,
                'departmentId': item.department.id,
                'departmentName': item.department.name,
            }
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportInfo(request):
        priceGte = request.GET.get('pricegte')
        priceLte = request.GET.get('pricelte')
        bid = request.GET.get('bid')
        departmentId = request.GET.get('departmentId')
        status = request.GET.get('status')
        type1 = request.GET.get('type')

        query = Q()

        if status == "停用":
            query = query & Q(status=0)
        elif status == "正常":
            query = query & Q(status=1)
        elif status == '使用中':
            query = query & Q(status=2)
        elif status == "占用中":
            query = query & Q(status=3)
        elif status == "查看全部":
            pass
        else:
            query = query & ~Q(status=0)
        if BaseView.isExist(priceLte):
            query = query & Q(price__lte=priceLte)
        if BaseView.isExist(priceGte):
            query = query & Q(price__gte=priceGte)
        if BaseView.isExist(bid):
            query = query & Q(bid__contains=bid)
        if BaseView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if BaseView.isExist(type1):
            if type1 == "查看全部":
                pass
            else:
                query = query & Q(type__contains=type1)
        data = models.Beds.objects.filter(query).order_by("id")
        resl = []
        for item in list(data):
            a = int(item.status)
            b = ""
            if a == 0:
                b = "停用"
            elif a == 1:
                b = "正常"
            elif a == 2:
                b = "使用中"
            elif a == 3:
                b = "占用中"
            else:
                b = "其他"
            temp = {
                'id': item.id,
                'bid': item.bid,
                'price': item.price,
                'type': item.type,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'status': b,
                'departmentName': item.department.name,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('床位列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                              ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    def addInfo(request):
        models.Beds.objects.create(
            bid=request.POST.get('bid'),
            price=request.POST.get('price'),
            status=request.POST.get('status'),
            type=request.POST.get('type'),
            department=models.Departments.objects.filter(id=request.POST.get('departmentId')).first(),
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def updInfo(request):
        a = request.POST.get('status')
        if a == "停用":
            b = 0
        elif a == "正常":
            b = 1
        elif a == "使用中":
            b = 2
        elif a == "占用中":
            b = 3
        models.Beds.objects.filter(
            id=request.POST.get('id')
        ).update(
            bid=request.POST.get('bid'),
            price=request.POST.get('price'),
            status=b,
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            department=models.Departments.objects.filter(id=request.POST.get('departmentId')).first(),
        )
        return BaseView.success()

    def delInfo(request):
        if int(models.Beds.objects.filter(id=request.POST.get('id')).first().status) == 2 or \
                int(models.Beds.objects.filter(id=request.POST.get('id')).first().status) == 3:
            return BaseView.warn('床位被占用暂无法移除')
        else:
            models.Beds.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()


# 住院记录管理
class HospitalizationLogsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return HospitalizationLogsView.getInfo(request)
        elif module == 'page':
            return HospitalizationLogsView.getPageInfo(request)
        elif module == 'export':
            return HospitalizationLogsView.exportInfo(request)
        elif module == 'bed':
            return HospitalizationLogsView.getAvailableBeds(request)
        elif module == 'money':
            return HospitalizationLogsView.getMoneyInfo(request)
        elif module == 'medical':
            return HospitalizationLogsView.getPageMedicalInfos(request)
        elif module == 'deal':
            return HospitalizationLogsView.getDealInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return HospitalizationLogsView.addInfo(request)
        elif module == 'upd':
            return HospitalizationLogsView.updInfo(request)
        elif module == 'del':
            return HospitalizationLogsView.delInfo(request)
        elif module == 'addmoney':
            return HospitalizationLogsView.upAddPatientMoney(request)
        # 添加医嘱
        elif module == 'addma':
            return HospitalizationLogsView.addMedicalAdvice(request)
        elif module == 'out':
            return HospitalizationLogsView.updInHosInfo(request)
        elif module == 'delmoney':
            return HospitalizationLogsView.upMinusPatientMoney(request)
        elif module == 'exportdeal':
            return HospitalizationLogsView.exportDealInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.HospitalizationLogs.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'doctorId': data.doctor.id,
            'patientId': data.patient.id,
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
            'duringTime': data.duringTime,
            'registerId': data.register.id,
            'departmentId': data.department.id,
            'status': data.status,
        }
        if BaseView.isExist(data.hospitalizationStartTime):
            resl['hospitalizationStartTime'] = datetime.datetime.strftime(data.hospitalizationStartTime, "%Y-%m-%d")
        if BaseView.isExist(data.bed):
            resl['bedId'] = data.bed.id
        if BaseView.isExist(data.updateTime):
            resl['hospitalizationEndTime'] = datetime.datetime.strftime(data.hospitalizationEndTime,
                                                                        "%Y-%m-%d %H:%M:%S")
        else:
            resl['hospitalizationEndTime'] = ''
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageMedicalInfos(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        type1 = int(request.GET.get('type'))
        oid = request.GET.get('oid')
        patientName = request.GET.get('patientName')
        query = Q()
        if int(loginUser['type']) == 2:
            query = query & Q(inHospitalLog__patient__user__id=loginUser['userId'])
            query = query & (Q(inHospitalLog__status=2) | Q(inHospitalLog__status=3))
            query = query & (Q(type=3) | Q(type=4))
        if BaseView.isExist(patientName):
            query = query & (Q(inHospitalLog__patient__name=patientName) | Q(registerLog__patient__name=patientName))
        if type1 == 1:
            data = models.MedicalAdvice.objects.filter(query).order_by('startTime')
            paginator = Paginator(data, pageSize)
            resl1 = []
            for item in list(paginator.page(pageIndex)):
                if item.oid not in resl1:
                    resl1.append(item.oid)
            data = models.MedicalAdvice.objects.values('oid', 'content', 'type',
                                                       'inHospitalLog', 'registerLog').distinct().filter(query)
            paginator = Paginator(data, pageSize)
            resl = []
            for item in list(paginator.page(pageIndex)):
                temp = {}
                a = models.HospitalizationLogs.objects.filter(id=item['inHospitalLog']).exists()
                c = models.RegisterLogs.objects.filter(id=item['registerLog']).exists()
                if a:
                    a = models.HospitalizationLogs.objects.filter(id=item['inHospitalLog']).first()
                    if (int(a.status) == 2) or (int(a.status) == 3):
                        pass
                    else:
                        continue
                    temp['hospitalizationLogsId'] = a.id
                    if BaseView.isExist(a.bed):
                        temp['hospitalizationLogsBedsId'] = a.bed.id
                        temp['hospitalizationLogsBedsBid'] = a.bed.bid
                        if BaseView.isExist(a.hospitalizationStartTime):
                            temp['hospitalizationLogsHospitalizationStartTime'] = datetime.datetime.strftime(
                                a.hospitalizationStartTime, "%Y-%m-%d")
                    temp['departmentName'] = a.department.name
                    if BaseView.isExist(a.hospitalizationEndTime):
                        temp['hospitalizationLogsHospitalizationEndTime'] = datetime.datetime.strftime(
                            a.hospitalizationEndTime, "%Y-%m-%d")
                    else:
                        temp['hospitalizationLogsHospitalizationEndTime'] = ''
                elif c:
                    c = models.RegisterLogs.objects.filter(id=item['registerLog']).first()
                    if BaseView.isExist(c.department):
                        temp['departmentName'] = c.department.name
                if BaseView.isExist(models.MedicalAdvice.objects.filter(oid=item['oid']).first().createTime):
                    temp['createTime'] = datetime.datetime.strftime(
                        models.MedicalAdvice.objects.filter(oid=item['oid']).first().createTime, "%Y-%m-%d %H:%M:%S")
                temp.update({
                    'oid': item['oid'],
                    'startDoctorId': models.MedicalAdvice.objects.filter(oid=item['oid']).first().startDoctor.id,
                    'startDoctorName': models.MedicalAdvice.objects.filter(oid=item['oid']).first().startDoctor.name,
                    'startTime': datetime.datetime.strftime(models.MedicalAdvice.objects.filter(
                        oid=item['oid']).order_by('startTime').first().startTime, "%Y-%m-%d %H:%M"),
                    'type': item['type'],
                })
                temp['content'] = item['content']
                resl.append(temp)
            temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                      paginator.page(pageIndex).paginator.num_pages,
                                      paginator.count, resl)
            return BaseView.successData(temp)
        elif type1 == 2:
            query = query & Q(oid=oid)
            data = models.MedicalAdvice.objects.filter(query).order_by('startTime')
            paginator = Paginator(data, pageSize)
            resl = []
            for item in list(paginator.page(pageIndex)):
                temp = {}
                if BaseView.isExist(item.inHospitalLog):
                    if (int(item.inHospitalLog.status) == 2) or (int(item.inHospitalLog.status) == 3):
                        pass
                    else:
                        continue
                    temp['hospitalizationLogsId'] = item.inHospitalLog.id
                    if BaseView.isExist(item.inHospitalLog.bed):
                        temp['hospitalizationLogsBedsId'] = item.inHospitalLog.bed.id
                        temp['hospitalizationLogsBedsBid'] = item.inHospitalLog.bed.bid
                        if BaseView.isExist(item.inHospitalLog.hospitalizationStartTime):
                            temp['hospitalizationLogsHospitalizationStartTime'] = datetime.datetime.strftime(
                                item.inHospitalLog.hospitalizationStartTime, "%Y-%m-%d")
                        temp['hospitalizationLogsDepartmentName'] = item.inHospitalLog.department.name
                    if BaseView.isExist(item.inHospitalLog.hospitalizationEndTime):
                        temp['hospitalizationLogsHospitalizationEndTime'] = datetime.datetime.strftime(
                            item.inHospitalLog.hospitalizationEndTime, "%Y-%m-%d")
                    else:
                        temp['hospitalizationLogsHospitalizationEndTime'] = ''
                if BaseView.isExist(item.createTime):
                    temp['createTime'] = datetime.datetime.strftime(
                        item.createTime, "%Y-%m-%d %H:%M:%S")
                temp.update({
                    'id': item.id,
                    'oid': item.oid,
                    'startDoctorId': item.startDoctor.id,
                    'startDoctorName': item.startDoctor.name,
                    'startTime': datetime.datetime.strftime(item.startTime, "%Y-%m-%d %H:%M"),
                    'type': item.type,
                })
                if BaseView.isExist(item.endDoctor):
                    temp['endDoctorId'] = item.endDoctor.id
                    temp['endDoctorName'] = item.endDoctor.name
                if BaseView.isExist(item.endTime):
                    temp['endTime'] = datetime.datetime.strftime(item.endTime, "%Y-%m-%d %H:%M")
                else:
                    temp['endDoctorId'] = ''
                    temp['endDoctorName'] = ''
                    temp['endTime'] = ''
                if BaseView.isExist(item.medicine):
                    temp['medicineName'] = item.medicine.drugName
                    temp['medicineCommonName'] = item.medicine.commonName
                    temp['medicineUnit'] = item.medicine.unit
                temp['freq'] = item.freq
                temp['medication'] = item.medication
                temp['dose'] = item.dose
                temp['price'] = item.price
                temp['times'] = item.times
                temp['allFreq'] = item.allFreq
                if BaseView.isExist(item.freq) and BaseView.isExist(item.dose) and BaseView.isExist(item.times) \
                        and BaseView.isExist(item.medicine):
                    temp['use'] = "{}{}/次 {}次/{}天".format(item.dose, item.medicine.unit, item.times, item.freq)
                else:
                    temp['use'] = ''
                if BaseView.isExist(item.inspection):
                    temp['inspectionId'] = item.inspection.id
                    temp['inspectionName'] = item.inspection.name
                    temp['inspectionType'] = item.inspection.type
                    temp['inspectionContent'] = item.inspection.content
                    temp['inspectionTime'] = item.inspection.inspectTime
                    temp['inspectionPrice'] = item.inspection.price
                if BaseView.isExist(item.inspectPreTime):
                    temp['inspectPreTime'] = datetime.datetime.strftime(item.inspectPreTime, "%Y-%m-%d %H:%M")
                if BaseView.isExist(item.inspectTime):
                    temp['inspectTime'] = datetime.datetime.strftime(item.inspectTime, "%Y-%m-%d %H:%M")
                temp['content'] = item.content
                resl.append(temp)
            temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                      paginator.page(pageIndex).paginator.num_pages,
                                      paginator.count, resl)
            return BaseView.successData(temp)
        elif type1 == 3:
            query = query & Q(endTime__gte=datetime.datetime.now().date())
            query = query & Q(inHospitalLog__status=2)
            if models.MedicalAdvice.objects.filter(query).exists():
                resl = {'flag': 1}
                return BaseView.successData(resl)
            else:
                resl = {'flag': 2}
                return BaseView.successData(resl)
        elif type1 == 4:
            data = models.MedicalAdvice.objects.filter(query).order_by('startTime')
            paginator = Paginator(data, pageSize)
            resl1 = []
            for item in list(paginator.page(pageIndex)):
                if item.oid not in resl1:
                    resl1.append(item.oid)
            data = models.MedicalAdvice.objects.values('oid', 'content', 'type',
                                                       'inHospitalLog', 'registerLog').distinct().filter(query)
            paginator = Paginator(data, pageSize)
            resl = []
            for item in list(paginator.page(pageIndex)):
                temp = {}
                a = models.HospitalizationLogs.objects.filter(id=item['inHospitalLog']).exists()
                c = models.RegisterLogs.objects.filter(id=item['registerLog']).exists()
                if a:
                    a = models.HospitalizationLogs.objects.filter(id=item['inHospitalLog']).first()
                    temp['hospitalizationLogsId'] = a.id
                    if BaseView.isExist(a.bed):
                        temp['hospitalizationLogsBedsId'] = a.bed.id
                        temp['hospitalizationLogsBedsBid'] = a.bed.bid
                        if BaseView.isExist(a.hospitalizationStartTime):
                            temp['hospitalizationLogsHospitalizationStartTime'] = datetime.datetime.strftime(
                                a.hospitalizationStartTime, "%Y-%m-%d")
                    temp['departmentName'] = a.department.name
                    if BaseView.isExist(a.hospitalizationEndTime):
                        temp['hospitalizationLogsHospitalizationEndTime'] = datetime.datetime.strftime(
                            a.hospitalizationEndTime, "%Y-%m-%d")
                    else:
                        temp['hospitalizationLogsHospitalizationEndTime'] = ''
                elif c:
                    c = models.RegisterLogs.objects.filter(id=item['registerLog']).first()
                    if BaseView.isExist(c.department):
                        temp['departmentName'] = c.department.name
                if BaseView.isExist(models.MedicalAdvice.objects.filter(oid=item['oid']).first().createTime):
                    temp['createTime'] = datetime.datetime.strftime(
                        models.MedicalAdvice.objects.filter(oid=item['oid']).first().createTime, "%Y-%m-%d %H:%M:%S")
                temp.update({
                    'oid': item['oid'],
                    'startDoctorId': models.MedicalAdvice.objects.filter(oid=item['oid']).first().startDoctor.id,
                    'startDoctorName': models.MedicalAdvice.objects.filter(oid=item['oid']).first().startDoctor.name,
                    'startTime': datetime.datetime.strftime(models.MedicalAdvice.objects.filter(
                        oid=item['oid']).order_by('startTime').first().startTime, "%Y-%m-%d %H:%M"),
                    'type': item['type'],
                })
                temp['content'] = item['content']
                resl.append(temp)
            temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                      paginator.page(pageIndex).paginator.num_pages,
                                      paginator.count, resl)
            return BaseView.successData(temp)
        elif type1 == 5:
            query = query & Q(oid=oid)
            data = models.MedicalAdvice.objects.filter(query).order_by('startTime')
            paginator = Paginator(data, pageSize)
            resl = []
            for item in list(paginator.page(pageIndex)):
                temp = {}
                if BaseView.isExist(item.inHospitalLog):
                    temp['hospitalizationLogsId'] = item.inHospitalLog.id
                    if BaseView.isExist(item.inHospitalLog.bed):
                        temp['hospitalizationLogsBedsId'] = item.inHospitalLog.bed.id
                        temp['hospitalizationLogsBedsBid'] = item.inHospitalLog.bed.bid
                        if BaseView.isExist(item.inHospitalLog.hospitalizationStartTime):
                            temp['hospitalizationLogsHospitalizationStartTime'] = datetime.datetime.strftime(
                                item.inHospitalLog.hospitalizationStartTime, "%Y-%m-%d")
                        temp['hospitalizationLogsDepartmentName'] = item.inHospitalLog.department.name
                    if BaseView.isExist(item.inHospitalLog.hospitalizationEndTime):
                        temp['hospitalizationLogsHospitalizationEndTime'] = datetime.datetime.strftime(
                            item.inHospitalLog.hospitalizationEndTime, "%Y-%m-%d")
                    else:
                        temp['hospitalizationLogsHospitalizationEndTime'] = ''
                if BaseView.isExist(item.createTime):
                    temp['createTime'] = datetime.datetime.strftime(
                        item.createTime, "%Y-%m-%d %H:%M:%S")
                temp.update({
                    'id': item.id,
                    'oid': item.oid,
                    'startDoctorId': item.startDoctor.id,
                    'startDoctorName': item.startDoctor.name,
                    'startTime': datetime.datetime.strftime(item.startTime, "%Y-%m-%d %H:%M"),
                    'type': item.type,
                })
                if BaseView.isExist(item.endDoctor):
                    temp['endDoctorId'] = item.endDoctor.id
                    temp['endDoctorName'] = item.endDoctor.name
                if BaseView.isExist(item.endTime):
                    temp['endTime'] = datetime.datetime.strftime(item.endTime, "%Y-%m-%d %H:%M")
                else:
                    temp['endDoctorId'] = ''
                    temp['endDoctorName'] = ''
                    temp['endTime'] = ''
                if BaseView.isExist(item.medicine):
                    temp['medicineName'] = item.medicine.drugName
                    temp['medicineCommonName'] = item.medicine.commonName
                    temp['medicineUnit'] = item.medicine.unit
                temp['freq'] = item.freq
                temp['medication'] = item.medication
                temp['dose'] = item.dose
                temp['price'] = item.price
                temp['times'] = item.times
                temp['allFreq'] = item.allFreq
                if BaseView.isExist(item.freq) and BaseView.isExist(item.dose) and BaseView.isExist(item.times) \
                        and BaseView.isExist(item.medicine):
                    temp['use'] = "{}{}/次 {}次/{}天".format(item.dose, item.medicine.unit, item.times, item.freq)
                else:
                    temp['use'] = ''
                if BaseView.isExist(item.inspection):
                    temp['inspectionId'] = item.inspection.id
                    temp['inspectionName'] = item.inspection.name
                    temp['inspectionType'] = item.inspection.type
                    temp['inspectionContent'] = item.inspection.content
                    temp['inspectionTime'] = item.inspection.inspectTime
                    temp['inspectionPrice'] = item.inspection.price
                if BaseView.isExist(item.inspectPreTime):
                    temp['inspectPreTime'] = datetime.datetime.strftime(item.inspectPreTime, "%Y-%m-%d %H:%M")
                if BaseView.isExist(item.inspectTime):
                    temp['inspectTime'] = datetime.datetime.strftime(item.inspectTime, "%Y-%m-%d %H:%M")
                temp['content'] = item.content
                resl.append(temp)
            temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                      paginator.page(pageIndex).paginator.num_pages,
                                      paginator.count, resl)
            return BaseView.successData(temp)
        else:
            return SysView.error()

    def getDealInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        query = Q()
        query = query & Q(eWallet__user__id=loginUser['userId'])
        data = models.Dealing.objects.filter(query).order_by('-dealTime')
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'dealTime': datetime.datetime.strftime(item.dealTime, "%Y-%m-%d %H:%M:%S"),
                'id': item.id,
                'price': item.price,
                'type': item.type,
                'bedPrice': item.bedPrice,
                'paymethod': item.paymethod,
            }
            a = item.inHospitalLog
            b = item.medicalAdvice
            c = 0
            if BaseView.isExist(a):
                temp.update({
                    'inHospitalLogId': a.id,
                    'inHospitalStartTime': datetime.datetime.strftime(a.hospitalizationStartTime, "%Y-%m-%d"),
                    'inHospitalDepartmentName': a.department.name,
                    'duringTime': a.duringTime,
                })
                if BaseView.isExist(a.hospitalizationEndTime):
                    temp.update({
                        'inHospitalEndTime': datetime.datetime.strftime(a.hospitalizationEndTime, "%Y-%m-%d"),
                    })
                if BaseView.isExist(a.department.name):
                    c = 1
            if BaseView.isExist(b):
                temp.update({
                    'medicalAdviceId': b.id,
                    'medicalAdviceOid': b.oid,
                    'medicalAdviceType': b.type,
                })
                if c == 0:
                    temp.update({
                        'inHospitalDepartmentName': b.inHospitalLog.department.name,
                    })

            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def exportDealInfo(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        query = Q()
        query = query & Q(eWallet__user__id=loginUser['userId'])
        data = models.Dealing.objects.filter(query).order_by('-dealTime')
        resl = []
        patientName = loginUser['name']
        for item in list(data):
            temp = {
                'dealTime': datetime.datetime.strftime(item.dealTime, "%Y-%m-%d %H:%M:%S"),
                'id': item.id,
                'price': item.price,
                'type': item.type,
                'bedPrice': item.bedPrice,
                'paymethod': item.paymethod,
            }
            a = item.inHospitalLog
            b = item.medicalAdvice
            if BaseView.isExist(a):
                temp.update({
                    'inHospitalLogId': a.id,
                    'inHospitalStartTime': datetime.datetime.strftime(a.hospitalizationStartTime, "%Y-%m-%d"),
                    'inHospitalDepartment': a.department,
                    'duringTime': a.duringTime,
                })
                if BaseView.isExist(a.hospitalizationEndTime):
                    temp.update({
                        'inHospitalEndTime': datetime.datetime.strftime(a.hospitalizationEndTime, "%Y-%m-%d"),
                    })
            if BaseView.isExist(b):
                pass
            resl.append(temp)
        if resl:
            aa = '{}交易信息信息列表{:<19}.xlsx'.format(patientName, datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
            pf = pd.DataFrame(resl)
            order = list(resl[0].keys())
            pf = pf[order]
            file_path = pd.ExcelWriter(aa)
            pf.to_excel(file_path, encoding="utf-8", index=False)
            file_path.save()
            return BaseView.success('导出成功')
        return BaseView.error('导出错误')

    def getPageInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        departmentId = request.GET.get('departmentId')
        startTime1 = request.GET.get('startTime1')
        startTime2 = request.GET.get('startTime2')
        endTime1 = request.GET.get('endTime1')
        endTime2 = request.GET.get('endTime2')
        bedBid = request.GET.get('bedBid')
        status = request.GET.get('status')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        elif loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if SysView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if SysView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if SysView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if SysView.isExist(startTime1):
            query = query & Q(hospitalizationStartTime__gte=startTime1)
        if SysView.isExist(startTime2):
            query = query & Q(hospitalizationStartTime__lte=startTime2)
        if SysView.isExist(endTime1):
            query = query & Q(hospitalizationEndTime__gte=endTime1)
        if SysView.isExist(endTime2):
            query = query & Q(hospitalizationEndTime__lte=endTime2)
        if SysView.isExist(status):
            query = query & Q(status=status)
        else:
            query = query & (Q(status=1) | Q(status=2) | Q(status=3))
        if SysView.isExist(bedBid):
            query = query & Q(bed__bid__contains=bedBid)
        if loginUser['type'] == 2:
            data = models.HospitalizationLogs.objects.filter(query).order_by("-status")
        else:
            data = models.HospitalizationLogs.objects.filter(query).order_by("-createTime")

        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            if a == 1:
                b = "待入院"
            elif a == 0:
                b = "已出院/患者拒绝入院"
            elif a == 2:
                b = "已入院"
            elif a == 3:
                b = "待出院"
            else:
                b = ""
            temp = {
                'id': item.id,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerId': item.register.id,
                'registerFee': item.register.registerFee,
                'registerTime': datetime.datetime.strftime(item.register.registerTime, "%Y-%m-%d"),
                'status': b,
                'doctorId': item.doctor.id,
                'duringTime': item.duringTime,
                'doctorName': item.doctor.name,
                'doctorGender': item.doctor.gender,
                'doctorEducation': item.doctor.education,
                'doctorRegisterFee': item.doctor.registerFee,
                'doctorAge': item.doctor.age,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorDepartmentName': item.doctor.department.name,
                'patientId': item.patient.id,
                'patientName': item.patient.name,
                'patientGender': item.patient.gender,
                'patientAge': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'departmentId': item.department.id,
                'departmentName': item.department.name,
            }
            if BaseView.isExist(item.hospitalizationStartTime):
                temp['hospitalizationStartTime'] = datetime.datetime.strftime(item.hospitalizationStartTime, "%Y-%m-%d")
            if BaseView.isExist(item.bed):
                temp['bedDepartmentName'] = item.bed.department.name
                temp['bedId'] = item.bed.id
                temp['bedBid'] = item.bed.bid
                temp['bedType'] = item.bed.type
                temp['bedPrice'] = item.bed.price
            if BaseView.isExist(item.hospitalizationEndTime):
                temp['hospitalizationEndTime'] = datetime.datetime.strftime(item.hospitalizationEndTime,
                                                                            "%Y-%m-%d %H:%M:%S")
            else:
                temp['hospitalizationEndTime'] = ''
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def getAvailableBeds(request):
        departmentId = request.GET.get('departmentId')
        query = Q()
        query = query & Q(department__id=departmentId)
        query = query & Q(status=1)
        data = models.Beds.objects.filter(query).order_by('-createTime')
        resl = []
        for item in list(data):
            temp = {
                'bid': item.bid,
                'id': item.id,
                'price': item.price,
                'status': item.status,
                'info': str(item.bid) + '\t' + str(item.price) + '元',
            }
            resl.append(temp)
        return BaseView.successData(resl)

    def getMoneyInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        query = Q()
        if BaseView.isExist(request.GET.get('Id')):
            inHospitalId = request.GET.get('Id')
            patientUserId = models.HospitalizationLogs.objects.filter(id=inHospitalId).first().patient.user.id
            query = query & Q(user__id=patientUserId)
        else:
            query = query & Q(user__id=loginUser['userId'])
        data = models.EWallet.objects.filter(query).first().balance
        return BaseView.successData(data)

    def upAddPatientMoney(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        userId = loginUser['userId']
        paymethod = request.POST.get('paymethod')
        a = int(models.EWallet.objects.filter(user__id=userId).first().balance)
        if int(request.POST.get('addmoneynum')) == 0:
            return BaseView.error('充值金额输入错误')
        models.EWallet.objects.filter(
            user__id=userId
        ).update(
            balance=int(request.POST.get('addmoneynum')) + a
        )
        models.Dealing.objects.create(
            eWallet=models.EWallet.objects.filter(user__id=userId).first(),
            type='充值',
            price=int(request.POST.get('addmoneynum')),
            dealTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            paymethod=paymethod,
        )
        return BaseView.success('充值成功')

    def upMinusPatientMoney(request):
        loginUser = SysView.getLoginUser(request.POST.get('token'))
        userId = loginUser['userId']
        balance = models.EWallet.objects.filter(user__id=userId).first().balance
        paymethod = request.POST.get('paymethod')
        if balance == 0:
            return BaseView.error('钱包没有可提现金额')
        elif balance < int(request.POST.get('minusmoneynum')):
            return BaseView.error('提现失败')
        if int(request.POST.get('minusmoneynum')) == 0:
            return BaseView.error('提现金额输入错误')
        models.EWallet.objects.filter(
            user__id=userId
        ).update(
            balance=balance - int(request.POST.get('minusmoneynum'))
        )
        models.Dealing.objects.create(
            eWallet=models.EWallet.objects.filter(user__id=userId).first(),
            type='提现',
            price=int(request.POST.get('minusmoneynum')),
            dealTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            paymethod=paymethod,
        )
        return BaseView.success('提现成功')

    def exportInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        departmentId = request.GET.get('departmentId')
        startTime1 = request.GET.get('startTime1')
        startTime2 = request.GET.get('startTime2')
        endTime1 = request.GET.get('endTime1')
        endTime2 = request.GET.get('endTime2')
        bedBid = request.GET.get('bedBid')
        status = request.GET.get('status')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        elif loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if SysView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if SysView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if SysView.isExist(departmentId):
            query = query & Q(department__id=departmentId)
        if SysView.isExist(startTime1):
            query = query & Q(hospitalizationStartTime__gte=startTime1)
        if SysView.isExist(startTime2):
            query = query & Q(hospitalizationStartTime__lte=startTime2)
        if SysView.isExist(endTime1):
            query = query & Q(hospitalizationEndTime__gte=endTime1)
        if SysView.isExist(endTime2):
            query = query & Q(hospitalizationEndTime__lte=endTime2)
        if SysView.isExist(status):
            query = query & Q(status=status)
        if SysView.isExist(bedBid):
            query = query & Q(bed__bid__contains=bedBid)
        if loginUser['type'] == 2:
            data = models.HospitalizationLogs.objects.filter(query).order_by("-status")
        else:
            data = models.HospitalizationLogs.objects.filter(query).order_by("-createTime")

        resl = []
        for item in list(data):
            a = int(item.status)
            if a == 1:
                b = "待入院"
            elif a == 0:
                b = "已出院/患者拒绝入院"
            elif a == 2:
                b = "已入院"
            elif a == 3:
                b = "待出院"
            else:
                b = ''
            temp = {
                'id': item.id,
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerId': item.register.id,
                'registerFee': item.register.registerFee,
                'registerTime': datetime.datetime.strftime(item.register.registerTime, "%Y-%m-%d"),
                'status': b,
                'doctorId': item.doctor.id,
                'duringTime': item.duringTime,
                'doctorName': item.doctor.name,
                'doctorGender': item.doctor.gender,
                'doctorEducation': item.doctor.education,
                'doctorRegisterFee': item.doctor.registerFee,
                'doctorAge': item.doctor.age,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorDepartmentName': item.doctor.department.name,
                'patientId': item.patient.id,
                'patientName': item.patient.name,
                'patientGender': item.patient.gender,
                'patientAge': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'departmentId': item.department.id,
                'departmentName': item.department.name,
            }
            if BaseView.isExist(item.hospitalizationStartTime):
                temp['hospitalizationStartTime'] = datetime.datetime.strftime(item.hospitalizationStartTime, "%Y-%m-%d")
            else:
                temp['hospitalizationStartTime'] = ''
            if BaseView.isExist(item.bed):
                temp['bedDepartmentName'] = item.bed.department.name
                temp['bedId'] = item.bed.id
                temp['bedBid'] = item.bed.bid
                temp['bedType'] = item.bed.type
                temp['bedPrice'] = item.bed.price
            if BaseView.isExist(item.hospitalizationEndTime):
                temp['hospitalizationEndTime'] = datetime.datetime.strftime(item.hospitalizationEndTime,
                                                                            "%Y-%m-%d %H:%M:%S")
            else:
                temp['hospitalizationEndTime'] = ''
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        if resl:
            with open('住院信息列表{:<19}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                                                ), 'w', encoding='utf-8', newline='') as f:
                a = resl[0]
                b = [i for i in a]
                csv_writer = csv.DictWriter(f, fieldnames=b)
                csv_writer.writeheader()
                csv_writer.writerows(resl)
            return BaseView.success('导出成功')
        else:
            return BaseView.warn('导出失败')

    def addInfo(request):
        user = SysView.getLoginUser(request.POST.get('token'))
        # 考虑到是否可能被管理端使用，就没有删代码。else部分为门诊开具住院单使用部分
        if BaseView.isExist(request.POST.get('bedId')):
            c = models.HospitalizationLogs.objects.create(
                createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                patient=models.Patients.objects.filter(id=request.POST.get('patientId')).first(),
                doctor=models.Doctors.objects.filter(user__id=user['userId']).first(),
                bed=models.Beds.objects.filter(bid=request.POST.get('bedId')).first(),
                register=models.RegisterLogs.objects.filter(id=request.POST.get('registerId')).first(),
                status=request.POST.get('status'),
            )
            a = BaseView.isExist(request.POST.get('hospitalizationStartTime'))
            aa = request.POST.get('hospitalizationStartTime')
            aaa = datetime.datetime.strptime(aa, "%Y-%m-%d")
            b = BaseView.isExist(request.POST.get('hospitalizationEndTime'))
            bb = request.POST.get('hospitalizationEndTime')
            bbb = datetime.datetime.strptime(bb, "%Y-%m-%d")
            if a:
                models.HospitalizationLogs.objects.filter(id=c.id).update(
                    startTime=aa,
                )
            if b:
                models.HospitalizationLogs.objects.filter(id=c.id).update(
                    endTime=bb,
                )
            if a and b:
                models.HospitalizationLogs.objects.filter(id=c.id).update(
                    duringTime=int((bbb - aaa).days)
                )
            return BaseView.success()
        else:
            doctorName = request.POST.get('startDoctorName')
            departmentName = request.POST.get('inHosDept')
            oneDepartment = models.Departments.objects.filter(name=departmentName).first()
            if BaseView.isExist(oneDepartment):
                oneDoctor = models.Doctors.objects.filter(department__name=departmentName, name=doctorName).first()
                if BaseView.isExist(oneDoctor):
                    c = models.HospitalizationLogs.objects.create(
                        createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        patient=models.RegisterLogs.objects.filter(id=request.POST.get('registerId')).first().patient,
                        doctor=models.Doctors.objects.filter(id=oneDoctor.id).first(),
                        register=models.RegisterLogs.objects.filter(id=request.POST.get('registerId')).first(),
                        status=request.POST.get('status'),
                        department=models.Departments.objects.filter(id=oneDepartment.id).first(),
                    )
                    return BaseView.success()
                else:
                    return BaseView.error()
            else:
                return BaseView.error()

    @transaction.atomic
    def addMedicalAdvice(request):
        doctorId = request.POST.get('doctorId')
        sumprice = 0
        if int(request.POST.get('type')) == 1:
            commonNameList = request.POST.getlist('medicine_forms[medicine]')
            startTimeList = request.POST.getlist('medicine_forms[startTime]')
            endTimeList = request.POST.getlist('medicine_forms[endTime]')
            medicationList = request.POST.getlist('medicine_forms[medication]')
            freqList = request.POST.getlist('medicine_forms[freq]')
            timesList = request.POST.getlist('medicine_forms[times]')
            doseList = request.POST.getlist('medicine_forms[dose]')
            allFreqList = request.POST.getlist('medicine_forms[allFreq]')
            for i in range(len(commonNameList)):
                numm = int(doseList[i])\
                          * int(timesList[i]) * float(allFreqList[i]) / int(freqList[i])
                price = int(models.Medicine.objects.filter(
                        commonName=commonNameList[i]
                    ).first().price) * numm
                aaa = int(models.Medicine.objects.filter(commonName=commonNameList[i]).first().inventory)
                bbb = models.Medicine.objects.filter(commonName=commonNameList[i]).first().type
                if bbb == "停用药":
                    return BaseView.error('{}已停用'.format(commonNameList[i]))
                if aaa < numm:
                    return BaseView.error('药品{}库存不足，仅剩{}'.format(commonNameList[i], aaa))
                models.MedicalAdvice.objects.create(
                    oid=request.POST.get('oid'),
                    symptom=request.POST.get('symptom'),
                    diagnosis=request.POST.get('diagnosis'),
                    content=request.POST.get('content'),
                    type=request.POST.get('type'),
                    registerLog=models.RegisterLogs.objects.filter(id=int(request.POST.get('registerLog'))).first(),
                    medicine=models.Medicine.objects.filter(commonName=commonNameList[i]).first(),
                    medication=medicationList[i],
                    startTime=datetime.datetime.strptime(startTimeList[i], "%Y-%m-%d"),
                    endTime=datetime.datetime.strptime(endTimeList[i], "%Y-%m-%d"),
                    freq=int(freqList[i]),
                    times=int(timesList[i]),
                    createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    dose=int(doseList[i]),
                    startDoctor=models.Doctors.objects.filter(id=doctorId).first(),
                    allFreq=float(allFreqList[i]),
                    price=price,
                )
                models.Medicine.objects.filter(commonName=commonNameList[i]).update(
                    inventory=aaa - numm,
                )
        elif int(request.POST.get('type')) == 2:
            inspectNameList = request.POST.getlist('medicine_forms[inspectName]')
            startTimeList = request.POST.getlist('medicine_forms[startTime]')
            for i in range(len(inspectNameList)):
                price = int(models.Inspection.objects.filter(name=inspectNameList[i]).first().price)
                inspectTime = models.Inspection.objects.filter(name=inspectNameList[i]).first().inspectTime
                inspectPreTimeTemp = datetime.datetime.now() + datetime.timedelta(hours=inspectTime)
                inspectPreTimeTemp = inspectPreTimeTemp.strftime("%Y-%m-%d %H:%M:%S")
                models.MedicalAdvice.objects.create(
                    oid=request.POST.get('oid'),
                    diagnosis=request.POST.get('diagnosis'),
                    symptom=request.POST.get('symptom'),
                    type=request.POST.get('type'),
                    registerLog=models.RegisterLogs.objects.filter(id=int(request.POST.get('registerLog'))).first(),

                    inspection=models.Inspection.objects.filter(name=inspectNameList[i]).first(),
                    inspectPreTime=inspectPreTimeTemp,
                    startTime=startTimeList[i],
                    startDoctor=models.Doctors.objects.filter(id=doctorId).first(),
                    allFreq=1,
                    price=price,
                    createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
        elif int(request.POST.get('type')) == 3:
            userId = models.HospitalizationLogs.objects.filter(
                id=request.POST.get('inhospital_log')
            ).first().patient.user.id
            commonNameList = request.POST.getlist('medicine_forms[common_name]')
            startTimeList = request.POST.getlist('medicine_forms[start_time]')
            endTimeList = request.POST.getlist('medicine_forms[end_time]')
            medicationList = request.POST.getlist('medicine_forms[medication]')
            freqList = request.POST.getlist('medicine_forms[freq]')
            timesList = request.POST.getlist('medicine_forms[times]')
            doseList = request.POST.getlist('medicine_forms[dose]')
            price = 0
            for i in range(len(request.POST.getlist('medicine_forms[common_name]'))):
                numm = int(doseList[i])\
                          * int(timesList[i]) * relativedelta(datetime.timedelta(1) + datetime.datetime.strptime(endTimeList[i], '%Y-%m-%d'), datetime.datetime.strptime(startTimeList[i], '%Y-%m-%d')).days\
                          / int(freqList[i])
                price = int(models.Medicine.objects.filter(
                        commonName=commonNameList[i]
                    ).first().price) * numm
                aaa = int(models.Medicine.objects.filter(commonName=commonNameList[i]).first().inventory)
                bbb = models.Medicine.objects.filter(commonName=commonNameList[i]).first().type
                if bbb == "停用药":
                    return BaseView.error("{}已停用".format(commonNameList[i]))
                if aaa < numm:
                    return BaseView.error('药品{}库存不足，仅剩{}'.format(commonNameList[i], aaa))
                am = models.MedicalAdvice.objects.create(
                    oid=request.POST.get('oid'),
                    content=request.POST.get('content'),
                    type=request.POST.get('type'),
                    medicine=models.Medicine.objects.filter(commonName=commonNameList[i]).first(),
                    medication=medicationList[i],
                    startTime=datetime.datetime.strptime(startTimeList[i], "%Y-%m-%d"),
                    endTime=datetime.datetime.strptime(endTimeList[i], "%Y-%m-%d"),
                    freq=freqList[i],
                    times=timesList[i],
                    createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    dose=doseList[i],
                    startDoctor=models.Doctors.objects.filter(id=doctorId).first(),
                    allFreq=relativedelta(datetime.timedelta(1)
                                          + datetime.datetime.strptime(endTimeList[i], '%Y-%m-%d'),
                                          datetime.datetime.strptime(startTimeList[i], '%Y-%m-%d')).days,
                    inHospitalLog=models.HospitalizationLogs.objects.filter(
                        id=request.POST.get('inhospital_log')).first(),
                    price=price,
                )
                models.Medicine.objects.filter(commonName=commonNameList[i]).update(
                    inventory=aaa - numm,
                )
                models.Dealing.objects.create(
                    eWallet=models.EWallet.objects.filter(user__id=userId).first(),
                    price=-price,
                    medicalAdvice=am,
                    type='消费',
                    dealTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
                balance = int(models.EWallet.objects.filter(user__id=userId).first().balance)
                models.EWallet.objects.filter(user__id=userId).update(
                    balance=balance - price,
                )
        elif int(request.POST.get('type')) == 4:
            userId = models.HospitalizationLogs.objects.filter(
                id=request.POST.get('inhospital_log')
            ).first().patient.user.id
            inspectNameList = request.POST.getlist('medicine_forms[inspectionName]')
            startTimeList = request.POST.getlist('medicine_forms[start_time]')
            for i in range(len(inspectNameList)):
                price = int(models.Inspection.objects.filter(name=inspectNameList[i]).first().price)
                am = models.MedicalAdvice.objects.create(
                    oid=request.POST.get('oid'),
                    content=request.POST.get('content'),
                    type=request.POST.get('type'),
                    inspection=models.Inspection.objects.filter(
                        name=inspectNameList[i]
                    ).first(),
                    startTime=startTimeList[i],
                    startDoctor=models.Doctors.objects.filter(id=doctorId).first(),
                    allFreq=1,
                    price=price,
                    inHospitalLog=models.HospitalizationLogs.objects.filter(
                        id=request.POST.get('inhospital_log')
                    ).first(),
                )
                balance = int(models.EWallet.objects.filter(user__id=userId).first().balance)
                models.EWallet.objects.filter(user__id=userId).update(
                    balance=balance - price,
                )
                sumprice += price
                models.Dealing.objects.create(
                    eWallet=models.EWallet.objects.filter(user__id=userId).first(),
                    price=-price,
                    medicalAdvice=am,
                    type='消费',
                    dealTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
        else:
            return BaseView.error()
        return BaseView.success()

    def updInfo(request):
        models.HospitalizationLogs.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=request.POST.get('status'),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        if BaseView.isExist(request.POST.get('hospitalizationStartTime')):
            models.HospitalizationLogs.objects.filter(
                id=request.POST.get('id')
            ).update(
                hospitalizationStartTime=request.POST.get('hospitalizationStartTime'),
            )
        if BaseView.isExist(request.POST.get('originalBedId')):
            models.Beds.objects.filter(id=request.POST.get('originalBedId')).update(status=1)
        if BaseView.isExist(request.POST.get('bedId')):
            models.HospitalizationLogs.objects.filter(id=request.POST.get('id')).update(
                bed=request.POST.get('bedId'),
            )
            models.Beds.objects.filter(id=request.POST.get('bedId')).update(status=2)
            userId = models.HospitalizationLogs.objects.filter(id=request.POST.get('id')).first().patient.user.id
            daynum = int((datetime.datetime.now().date() -
                          models.HospitalizationLogs.objects.filter(
                              id=request.POST.get('id')
                          ).first().hospitalizationStartTime).days)
            bedPrice = models.HospitalizationLogs.objects.filter(id=request.POST.get('id')).first().bed.price
            price = daynum * bedPrice
            balance = int(models.EWallet.objects.filter(user__id=userId).first().balance)
            models.EWallet.objects.filter(user__id=userId).update(
                balance=balance - price,
            )
            if BaseView.isExist(request.POST.get('originalBedId')):
                models.Dealing.objects.create(
                    type='消费',
                    eWallet=models.EWallet.objects.filter(user__id=userId).first(),
                    inHospitalLog=models.HospitalizationLogs.objects.filter(id=request.POST.get('id')).first(),
                    bedPrice=bedPrice,
                    price=-price,
                    dealTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
        if SysView.isExist(request.POST.get('hospitalizationEndTime')):
            models.HospitalizationLogs.objects.filter(
                id=request.POST.get('id')
            ).update(
                hospitalizationEndTime=request.POST.get('hospitalizationEndTime'),
            )
            if SysView.isExist(request.POST.get('hospitalizationStartTime')):
                date1 = datetime.datetime.strptime(request.POST.get('hospitalizationStartTime'), "%Y-%m-%d")
                date2 = datetime.datetime.strptime(request.POST.get('hospitalizationEndTime'), "%Y-%m-%d")
                diff = date2 - date1
                day = int(diff.days)
                models.HospitalizationLogs.objects.filter(
                    id=request.POST.get('id')
                ).update(
                    duringTime=day,
                )
        return BaseView.success()

    def updInHosInfo(request):
        inHospitalLogId = request.POST.get('inHospitalLog')
        patientUserId = models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first().patient.user.id
        balance = int(models.EWallet.objects.filter(user__id=patientUserId).first().balance)
        a = datetime.datetime.now()
        query = Q()
        query = query & Q(endTime__gte=a) & Q(inHospitalLog__id=inHospitalLogId)
        flag = int(request.POST.get('flag'))

        if models.Dealing.objects.filter(inHospitalLog=inHospitalLogId).exists():
            a = models.Dealing.objects.filter(inHospitalLog=inHospitalLogId).order_by('-dealTime').first().dealTime
            bedPrice = int(models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first().bed.price)
            dat = int((datetime.datetime.now() - a).days)
            price = bedPrice * dat
            if dat == 0:
                pass
            else:
                models.Dealing.objects.create(
                    inHospitalLog=models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first(),
                    price=-price,
                    bedPrice=bedPrice,
                    dealTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    eWallet=models.EWallet.objects.filter(user__id=patientUserId).first(),
                    type="消费",
                )
                b = int(models.EWallet.objects.filter(user__id=patientUserId).first().balance)
                models.EWallet.objects.filter(user__id=patientUserId).update(
                    balance=b - price,
                )
        else:
            startTime = models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first().hospitalizationStartTime
            bedPrice = int(models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first().bed.price)
            dat = int((datetime.datetime.now().date() - startTime).days)
            price = bedPrice * dat
            if dat == 0:
                pass
            else:
                models.Dealing.objects.create(
                    type='消费',
                    eWallet=models.EWallet.objects.filter(user__id=patientUserId).first(),
                    dealTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    price=-price,
                    bedPrice=bedPrice,
                    inHospitalLog=models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first(),
                )
                b = int(models.EWallet.objects.filter(user__id=patientUserId).first().balance)
                models.EWallet.objects.filter(user__id=patientUserId).update(
                    balance=b - price,
                )
        balance = int(models.EWallet.objects.filter(user__id=patientUserId).first().balance)
        if flag == 1:
            models.HospitalizationLogs.objects.filter(id=inHospitalLogId).update(
                status=3
            )
            return BaseView.success('执行成功')
        elif flag == 2:
            if balance >= 0:
                models.HospitalizationLogs.objects.filter(id=inHospitalLogId).update(
                    status=0,
                )
                models.EWallet.objects.filter(user__id=patientUserId).update(
                    balance=0,
                )
                bedId = models.HospitalizationLogs.objects.filter(id=inHospitalLogId).first().bed.id
                models.Beds.objects.filter(id=bedId).update(
                    status=1,
                )
                return BaseView.success('确认出院成功')
            else:
                return BaseView.error('请缴清所有费用')
        else:
            return BaseView.error('处理失败')

    def delInfo(request):
        models.HospitalizationLogs.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()


# 排队管理
class QueueLogsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return QueueLogsView.getInfo(request)
        elif module == 'page':
            return QueueLogsView.getPageInfo(request)
        elif module == 'select':
            return QueueLogsView.selectInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return QueueLogsView.addInfo(request)
        elif module == 'remove':
            return QueueLogsView.removeInfo(request)
        elif module == 'del':
            return QueueLogsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        data = models.RegisterLogs.objects.filter(id=request.GET.get('id')).first()
        resl = {
            'id': data.id,
            'registerTime': datetime.datetime.strftime(data.registerTime, "%Y-%m-%d"),
            'createTime': datetime.datetime.strftime(data.createTime, "%Y-%m-%d %H:%M:%S"),
            'registerFee': data.registerFee,
            'status': data.status,
            'patientId': data.patient.id,
            'doctorId': data.doctor.id,
        }
        if BaseView.isExist(data.updateTime):
            resl['updateTime'] = datetime.datetime.strftime(data.updateTime, "%Y-%m-%d %H:%M:%S")
        else:
            resl['updateTime'] = ''
        return BaseView.successData(resl)

    def getPageInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        registerTime = request.GET.get('registerTime')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        if loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if BaseView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if BaseView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if BaseView.isExist(registerTime):
            query = query & Q(registerTime=registerTime)
        data = models.RegisterLogs.objects.filter(query).order_by("-createTime")
        paginator = Paginator(data, pageSize)
        resl = []
        for item in list(paginator.page(pageIndex)):
            a = int(item.status)
            if a == 0:
                b = '账号已注销'
            elif a == 1:
                b = '正常'
            else:
                b = ''
            temp = {
                'id': item.id,
                'registerTime': datetime.datetime.strftime(item.registerTime, "%Y-%m-%d"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerFee': item.registerFee,
                'status': data.status,
                'patientId': item.patient.id,
                'patientName': item.patient.name,
                'patientGender': item.patient.gender,
                'patientAge': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'doctorId': item.doctor.id,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorName': item.doctor.name,
                'doctorDepartmentName': item.doctor.department.name,
            }
            if BaseView.isExist(item.updateTime):
                temp['updateTime'] = datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S")
            else:
                temp['updateTime'] = ''
            resl.append(temp)
        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                  paginator.page(pageIndex).paginator.num_pages,
                                  paginator.count, resl)
        return BaseView.successData(temp)

    def selectInfo(request):
        loginUser = SysView.getLoginUser(request.GET.get('token'))
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('patientName')
        registerTime = request.GET.get('registerTime')

        query = Q()
        if loginUser['type'] == 1:
            query = query & Q(doctor__user__id=loginUser['userId'])
        if loginUser['type'] == 2:
            query = query & Q(patient__user__id=loginUser['userId'])
        if BaseView.isExist(doctorName):
            query = query & Q(doctor__name__contains=doctorName)
        if BaseView.isExist(patientName):
            query = query & Q(patient__name__contains=patientName)
        if BaseView.isExist(registerTime):
            query = query & Q(registerTime=registerTime)
        query = query & Q(status=1)
        data = models.RegisterLogs.objects.filter(query).order_by("updateTime")

        resl = []
        for item in data:
            temp = {
                'id': item.id,
                'registerTime': datetime.datetime.strftime(item.registerTime, "%Y-%m-%d"),
                'createTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'registerFee': item.registerFee,
                'patientId': item.patient.id,
                'name': item.patient.name,
                'patientGender': item.patient.gender,
                'age': item.patient.age,
                'patientPhone': item.patient.phone,
                'patientAddress': item.patient.address,
                'patientIdNumber': item.patient.idNumber,
                'doctorId': item.doctor.id,
                'doctorJob': item.doctor.job,
                'doctorPhone': item.doctor.phone,
                'doctorName': item.doctor.name,
                'gender': item.patient.gender,
                'updateTime': datetime.datetime.strftime(item.updateTime, "%Y-%m-%d %H:%M:%S"),
            }
            resl.append(temp)
        return BaseView.successData(resl)

    def addInfo(request):

        models.RegisterLogs.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=1,
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def removeInfo(request):
        models.RegisterLogs.objects.filter(
            id=request.POST.get('id')
        ).update(
            status=2,
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return BaseView.success()

    def delInfo(request):
        return BaseView.success()


# 处方管理
class PrescriptionView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'page':
            return PrescriptionView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return PrescriptionView.addInfo(request)
        elif module == 'upd':
            return PrescriptionView.updInfo(request)
        elif module == 'del':
            return PrescriptionView.delInfo(request)
        elif module == 'info':
            return PrescriptionView.getInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        test = request.POST.get('oid')
        data = models.MedicalAdvice.objects.filter(
            oid=request.POST.get('oid'),
            type=1)

        MedicineInfos = []

        totalprice = 0

        for item in data:
            temp = {
                'medicine': item.medicine.drugName,
                'freq': str(item.freq)+'天'+str(item.times)+'次',
                'medication': item.medication,
                'dose': item.dose,
                'fee': item.price,
        }
            totalprice = totalprice+item.price
            MedicineInfos.append(temp)

        medicalAdvice = {
            'startDoctorName':data[0].startDoctor.name,
            'oid' : data[0].oid,
            'content' : data[0].content,
            'totalprice': str(totalprice)+'元',
            'time': datetime.datetime.strftime(data[0].createTime, "%Y-%m-%d %H:%M:%S"),
        }

        resl={
            'MedicineInfos': MedicineInfos,
            'medicalAdvice': medicalAdvice,
        }
        return BaseView.successData(resl)

    def getPageInfo(request):


        loginUser = SysView.getLoginUser(request.GET.get('token'))
        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('name')

        qruery = Q()

        if loginUser['type'] == 1:
            qruery = qruery & Q(registerLog__doctor__user__id=loginUser['userId'])
            qruery = qruery & Q(registerLog__doctor__name__contains=loginUser['userName'])

        if loginUser['type'] == 2:
            qruery = qruery & Q(registerLog__patient__user__id=loginUser['userId'])
            qruery = qruery & Q(registerLog__patient__name__contains=loginUser['userName'])
        qruery = qruery & Q(type=1)
        data = models.MedicalAdvice.objects.filter(qruery).order_by("-createTime")
        paginator = Paginator(data, pageSize)

        resl = []
        oid_list = []
        for item in list(paginator.page(pageIndex)):
            if item.oid in oid_list:
                continue
            else:
                temp = {
                    'oid': item.oid,
                    'presTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                    'doctorJob': item.startDoctor.job,
                    'doctorName': item.startDoctor.name,
                    'doctorOfficeName': item.startDoctor.department.name,
                }
                resl.append(temp)
                oid_list.append(item.oid)

        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):
        return BaseView.success()

    def updInfo(request):
        return BaseView.success()

    def delInfo(request):
        return BaseView.success()


# 检查报告管理
class ReportsView(BaseView):
    def get(self, request, module, *args, **kwargs):
        if module == 'info':
            return ReportsView.getInfo(request)
        elif module == 'page':
            return ReportsView.getPageInfo(request)
        else:
            return BaseView.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return ReportsView.addInfo(request)
        elif module == 'upd':
            return ReportsView.updInfo(request)
        elif module == 'del':
            return ReportsView.delInfo(request)
        else:
            return BaseView.error()

    def getInfo(request):
        return BaseView.success()

    def getPageInfo(request):

        loginUser = SysView.getLoginUser(request.GET.get('token'))

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        doctorName = request.GET.get('doctorName')
        patientName = request.GET.get('paientName')

        qruery = Q()

        if loginUser['type'] == 1:
            qruery = qruery & Q(registerLog__doctor__user__id=loginUser['userId'])
            qruery = qruery & Q(registerLog__doctor__name__contains=loginUser['userName'])

        if loginUser['type'] == 2:
            qruery = qruery & Q(registerLog__patient__user__id=loginUser['userId'])
            qruery = qruery & Q(registerLog__patient__name__contains=loginUser['userName'])

        qruery = qruery & Q(type=2)
        # 这里修改了一下，医生姓名在医师表中
        if BaseView.isExist(doctorName):
            qruery = qruery & Q(registerLog__doctor__name__contains=doctorName)

        if BaseView.isExist(patientName):
            qruery = qruery & Q(registerLog__patient__name__contains=patientName)

        data = models.MedicalAdvice.objects.filter(qruery).order_by("-endTime")

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'checkItem': item.inspection.name,
                'checkTime': datetime.datetime.strftime(item.createTime, "%Y-%m-%d %H:%M:%S"),
                'repoTime': datetime.datetime.strftime(item.inspectPreTime, "%Y-%m-%d %H:%M:%S"),
            }
            resl.append(temp)

        temp = BaseView.parsePage(int(pageIndex), int(pageSize),
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        return BaseView.success()

    def updInfo(request):
        return BaseView.success()

    def delInfo(request):
        return BaseView.success()

