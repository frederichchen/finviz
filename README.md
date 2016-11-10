# Finviz：一个财政数据可视化显示的小玩意儿

## 构想

用可视化的方式展现财政数据的情况，帮助审计人员快速直观的读懂数据。

## 系统要求

1. 后台采用 Python3 + Flask 框架开发，以图简便。数据库采用 MySQL 。
2. 前台使用 jQuery 来执行 Ajax 查询，使用百度 ECharts 来显示图表。

在使用的时候，必须首先通过 Python 的包管理工具例如 pip 来安装 pymysql3 、flask 和 simplejson 三个包。

## 运行

运行之前请修改 app/config 目录下的 db.json 文件，将 MySQL 的用户名、密码和数据库等参数配置好。

在命令行下执行 python run.py ，然后访问 http://127.0.0.1:5000/ 即可。
