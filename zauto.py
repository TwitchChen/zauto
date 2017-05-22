#coding:utf-8
from flask import Flask,request
from flask import jsonify
from common.check_data import check
from zbxmod import zbx_add_host,zbx_login,zbx_delete_host,zbx_add_maintenance,zbx_delete_maintenance
from common.config import Config

app = Flask(__name__)
conf = Config()
##zauto说明
@app.route('/',methods=['POST'])
@app.route('/zauto',methods=['POST'])
def zauto():
    msg = {
        "msg":u"zabbix auto api",
        "status_code":200
    }
    return jsonify(msg),200

##hosts监控添加与删除
@app.route('/zauto/hosts')
def zauto_hosts():
    msg = {
        "msg":u"add or delete hosts monitor",
        "status_code":200
    }
    return jsonify(msg), 200

@app.route('/zauto/hosts/add',methods=["POST"])
@check()
def hosts_add():
    user = conf.zbx_user
    pwd = conf.zbj_pwd
    people_name = u"蹇尚翀/陈浩"
    data = eval(request.get_data())
    data = data["payload"]
    person = data["person"]
    if person:
        return jsonify({"msg":"person hosts can not add to zabbix", "status_code": 400}), 400
    region = data['region']
    ip = data['ip']
    name = data['name']
    if region == 'cqzb':
        url = conf.zbx_offline_server
        group = 'cqzb'
        template_name = 'linux7 system base template'
    elif region == 'bjzw':
        url = conf.zbx_online_server
        group = 'bjzw'
        template_name = 'linux7 system base template'
    elif region == 'bjyz':
        url = conf.zbx_online_server
        group = 'bjyz'
        template_name = 'linux7 system base template'
    elif region == 'tjhy':
        url = conf.zbx_online_server
        group = 'tjhy-pref-zbj'
        template_name = 'tjhy linux template for pref'
    else:
        url = conf.zbx_online_server
        group = 'Discovered hosts'
        template_name = 'linux7 system base template'
    zapi = zbx_login.login(url,user,pwd)
    zadd = zbx_add_host.zbx_add_hosts(zapi)
    if zadd.hostexist(ip,name):
        return jsonify({"msg":"host:%s or ip:%s already in zabbix"%(name,ip), "status_code":422}),422
    group_id_list, template_id_list = zadd.group_template_id(group, template_name)
    info, code = zadd.zabbix_add_host(name, ip, people_name, template_id_list,group_id_list)
    return jsonify({"msg":info,"status_code":code}),code

@app.route('/zauto/hosts/delete', methods=['POST'])
@check()
def hosts_delete():
    user = conf.zbx_user
    pwd = conf.zbj_pwd
    data = eval(request.get_data())
    data = data["payload"]
    region = data['region']
    ip = data['ip']
    if region == 'cqzb':
        url = conf.zbx_offline_server
    else:
        url = conf.zbx_online_server
    zapi = zbx_login.login(url,user,pwd)
    zdelete = zbx_delete_host.zbx_del_hosts(zapi)
    response = zdelete.host_interface_get(ip)
    if response:
        hostid = response[0]['hostid']
        zdelete.host_delete(hostid)
        return jsonify({"msg":"delete host success", "status_code":200}),200
    else:
        return jsonify({"msg":"host does not exists", "status_code":404}),404

##维护添加与删除
@app.route('/zauto/maintenance')
@check()
def zauto_maintenance():
    msg = {
        "msg":u"zabbix 维护，支持添加及删除维护",
        "status_code":200
    }
    return jsonify(msg),200

@app.route('/zauto/maintenance/add', methods=['POST'])
@check()
def maintenance_add():
    user = conf.zbx_user
    pwd = conf.zbj_pwd
    data = eval(request.get_data())
    data = data["payload"]
    region = data['region']
    ip = data['ip']
    if region == 'cqzb':
        url = conf.zbx_offline_server
    else:
        url = conf.zbx_online_server
    zapi = zbx_login.login(url, user, pwd)
    zadd = zbx_add_maintenance.zbx_add_main(zapi)
    response = zadd.host_interface_get(ip)
    if response:
        hostid = response[0]['hostid']
        return zadd.add_maintenance(hostid)
    else:
        return jsonify({"msg":"host not exists", "status_code":404}),404

@app.route('/zauto/maintenance/delete', methods=['POST'])
@check()
def maintenance_delete():
    user = conf.zbx_user
    pwd = conf.zbj_pwd
    data = eval(request.get_data())
    data = data["payload"]
    region = data['region']
    ip = data['ip']
    if region == 'cqzb':
        url = conf.zbx_offline_server
    else:
        url = conf.zbx_online_server
    zapi = zbx_login.login(url, user, pwd)
    zdelete = zbx_delete_maintenance.zbx_delete_main(zapi)
    response = zdelete.host_interface_get(ip)
    if response:
        hostid = response[0]['hostid']
        maintenanceid = zdelete.get_maintenance(hostid)
        if maintenanceid:
            maintenanceid = maintenanceid[0]['maintenanceid']
            return zdelete.delete_maintenance(maintenanceid)
        else:
            return jsonify({"msg": "mantenance not exists", "status_code": 404}), 404
    else:
        return jsonify({"msg":"host not exists", "status_code":404}),404

if __name__ == '__main__':
    app.run("0.0.0.0",5000)
