# TaskPublish
## 简介
采用Django作为后端，vue框架作为前端，实现的《召集令》原型系统。主要包含用户管理、任务发布和接收、数据分析等功能。
## 项目构建
Django相关依赖：            
```
pip install django          # django框架
pip install mysqlclient     # mysql相关
pip install django-cors-headers     # 跨域访问
```
vue相关：          
```
cd client
npm install 
npm run build
```
启动程序：
```
python manage.py runserver
```