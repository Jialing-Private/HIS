# HIS

#### 介绍
信息系统小组作业——医院信息系统HIS


#### 安装教程

1.  下载代码
2.  npm install安装依赖

#### 使用说明

1.  在server/server/setting.py中将数据库账号密码改为自己的账号密码
2.  在mysql数据库创建一个名为his的数据库
3.  进入server文件下，控制台执行python manage.py migrate，python manage.py makemigrations，python manage.py migrate
4.  在his数据库中导入测试数据
5.  进入server文件下，控制台命令python manage.py runserver 127.0.0.1:8000
6.  进入client_inhos文件下，控制台命令npm install，npm run serve
7.  进入manage文件下，控制台命令npm install，npm run serve
