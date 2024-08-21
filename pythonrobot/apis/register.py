import json

import requests
from flask import Blueprint, render_template, request, redirect, jsonify, Flask

from pythonrobot.util.util import ResMsg, ResponseMessage,sql

rs = Blueprint("register",__name__)

@rs.route('/register',methods=['POST'])
def register():
    """
       username字段为用户名
       user_id 字段为命名id
       phone字段为用户手机号码
       :return:
       """
    #获取用户请求信息
    data = request.get_json()
    avatar = data['avatar']
    avatarDesc=data['avatarDesc']
    nickname=data['nickname']
    phone = data['phone']
    status = data['status']

    #实例化响应状态码
    res = ResMsg()

    #响应data数据为空，返回参数不正确，状态码40002
    if not data:
        res.update(msg=ResponseMessage.INVALID_PARAMETER, code=40002, data=data)
        json_data = json.dumps(res.data, ensure_ascii=False)
        return json_data

    #执行核心算法语句，对信息存入表中
    SQL=sql()
    result = SQL.fetch_one(f"insert into userdata(avatar,avatarDesc,nickname,phone,status) values('{avatar}','{avatarDesc}','{nickname}','{phone}','{status}');")
    res.update(msg=f"{ResponseMessage.SUCCESS},{result}", data=data)
    json_data = json.dumps(res.data,ensure_ascii=False)

    #用户访问完后，自动访问本地服务接口，执行访问云端api操作
    second_api = requests.post("http://127.0.0.1:5000/cloud_server",json=json_data)

    return json_data










