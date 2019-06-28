## 文档
[django后台网站开发中文文档](https://docs.djangoproject.com/zh-hans/2.2/ "django中文文档")

[highcharts网页图表生成](https://www.runoob.com/highcharts/highcharts-tutorial.html "highcharts菜鸟教程")

[reportlab生成PDF图表](https://www.reportlab.com/docs/reportlab-userguide.pdf "reportlab user guide")

## 注意事项
```
时间仓促，未能集成cookie模块到登录访问控制中，
因此系统的登录其实只是虚有其表，不登录也可以访问网站其他网址。
```

## 如何使用
由于时间仓促，未能将项目依赖打包到虚拟环境venv中，所以需要手动安装依赖，但也非常简单

安装`python3.6`及以上版本

安装项目依赖，在lab3-wms根目录下执行`pip install -r requirements.txt`即可

进入`lab3-wms`根目录执行`python manage.py runserver`运行服务器

在浏览器中输入`http://127.0.0.1:8000/`即可，初始登录用户名为`ljq'，密码为`fuck`

## ER图

![员工工资管理系统ER图](image/ssm_ER.png "员工工资管理系统ER图")

## 登录

![登录界面](image/wms-login.jpg "登录界面")

## 主页

![主页](image/wms-index.jpg "主页")

## 部门管理主页

![部门管理主页](image/wms-department-index.jpg "部门管理主页")

## 增加部门

![增加部门](image/wms-department-create.jpg "增加部门")

## 修改部门

![修改部门](image/wms-department-update.jpg "修改部门")

## 搜索部门

![搜索部门](image/wms-department-search.jpg "搜索部门")

## 部门报表PDF生成

![部门报表](image/wms-department-table.jpg "部门报表")

## 特色功能饼状图

![部门人数对比](image/wms-department-number.jpg "部门人数对比")

![部门最低薪资对比](image/wms-department-minimum-wage.jpg "部门最低薪资对比")
