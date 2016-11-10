##################################################################################
#   本文件是用来进行导航的，将 index 页面导航到 /static/templates/treemap.html         #
#   对于 /treemap_data 文件，查询 MySQL 数据库，将结果组装成 JSON 返回                  #
##################################################################################

from flask import render_template, request
import pymysql
import simplejson as json
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('treemap.html')

@app.route('/treemap_data')
def treemap_data():
    with open("/home/frederich/finviz/app/config/db.json") as conf:    
        dbconfig = json.load(conf)
    conn = pymysql.connect(host=dbconfig["host"], user=dbconfig["user"], passwd=dbconfig["passwd"], db=dbconfig["db"], charset=dbconfig["charset"])
    cur = conn.cursor()
    data = {}
    # 接下来建立一个三层的 dict ，每一层都有一个 values 数组表示指标数和支付数，下面一层为其子科目。
    cur.execute("SELECT concat(xianqu, '.', lei) as lei, kuan, xiang, zhibiao, zhichu FROM guantong")
    for r in cur:
        zhibiao = round(r[3]/10000,2)
        zhifu = round(r[4]/10000,2)
        if r[0] in data:        
            data[r[0]]["values"][0] += zhibiao
            data[r[0]]["values"][1] += zhifu
        else:
            data[r[0]] = {}
            data[r[0]]["values"] = [zhibiao, zhifu]
    
        if r[1] in data[r[0]]:
            data[r[0]][r[1]]["values"][0] += zhibiao
            data[r[0]][r[1]]["values"][1] += zhifu
        else:
            data[r[0]][r[1]] = {}
            data[r[0]][r[1]]["values"] = [zhibiao, zhifu]

        if r[2] in data[r[0]][r[1]]:
            data[r[0]][r[1]][r[2]]["values"][0] += zhibiao
            data[r[0]][r[1]][r[2]]["values"][1] += zhifu
        else:
            data[r[0]][r[1]][r[2]] = {}
            data[r[0]][r[1]][r[2]]["values"] = [zhibiao, zhifu]
        
    cur.close()
    conn.close()
    return json.dumps(data, ensure_ascii=False)


@app.route('/sankey_data')
def sankey_data():
    with open("/home/frederich/finviz/app/config/db.json") as conf:    
        dbconfig = json.load(conf)
    conn = pymysql.connect(host=dbconfig["host"], user=dbconfig["user"], passwd=dbconfig["passwd"], db=dbconfig["db"], charset=dbconfig["charset"])
    cur = conn.cursor()
    data = {}
    # 获取传过来的地区和类款项参数
    xianqu = request.args.get('xianqu')
    lei = request.args.get('lei')
    kuan = request.args.get('kuan')
    xiang = request.args.get('xiang')
    statement = "SELECT kuan, xiang, danwei, zhichu FROM guantong where xianqu=\'" + xianqu + "\' and lei=\'" + lei + "\' and kuan=\'" + kuan + "\'"
    # ‘项’不是必须的，如果有就加上
    if xiang:
        statement += " and xiang=\'" + xiang +"\'"
    cur.execute(statement)
    for r in cur:
        zhifu = round(r[3]/10000,2)
        if r[0] not in data:
            data[r[0]] = {}
            
        if r[1] in data[r[0]]:
            data[r[0]][r[1]]["value"] += zhifu
        else:
            data[r[0]][r[1]] = {}
            data[r[0]][r[1]]["value"] = zhifu

        if r[2] in data[r[0]][r[1]]:
            data[r[0]][r[1]][r[2]]["value"] += zhifu
        else:
            data[r[0]][r[1]][r[2]] = {}
            data[r[0]][r[1]][r[2]]["value"] = zhifu
        
    cur.close()
    conn.close()

    # 接下来读取 data ，将其转换成 echarts 要求的数据类型，并以JSON格式返回
    nodes = [];
    links = [];
    for n1 in data:
        nodes.append(dict({"name": n1}))
        for n2 in data[n1]:
            if n2 != "value":
                nodes.append({"name": n2})
                links.append({"source": n1, "target": n2, "value": data[n1][n2]["value"]})
                for n3 in data[n1][n2]:
                    if n3 != "value":
                        nodes.append(dict({"name": n3}))
                        links.append({"source": n2, "target": n3, "value": data[n1][n2][n3]["value"]})

    return  "{\"nodes\":\n" + json.dumps(nodes, ensure_ascii=False) + ",\n\"links\":\n" + json.dumps(links, ensure_ascii=False) + "}"
