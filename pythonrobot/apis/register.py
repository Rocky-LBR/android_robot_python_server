import json
import time
import requests
from flask import Blueprint, render_template, request, redirect, jsonify, Flask
from pythonrobot.util.util import ResMsg, ResponseMessage, sql, cls_log, log_performance, ResponseCode

rs = Blueprint("register",__name__)


# #请求前执行性能监视
# @rs.before_request
# def start_timer():
#     request.start_time = time.time()
#
# # @rs.after_request
# # def log_request(register_logger):
# #     log_performance(register_logger)
# #     return


@rs.route('/register',methods=['POST'])
def register():
    """
       username字段为用户名
       user_id 字段为命名id
       phone字段为用户手机号码
       :return:
       """
    #获取用户请求信息
    register_logger = cls_log()
    current_url = request.url
    data = request.get_json()
    avatar = data['avatar']
    avatarDesc=data['avatarDesc']
    nickname=data['nickname']
    phone = data['phone']
    status = data['status']

    #实例化响应状态码
    res = ResMsg()
    #响应data数据为空，返回参数不正确，状态码Flase
    if not data:
        res.update(msg=ResponseMessage.INVALID_PARAMETER, code=ResponseMessage.FAIL, data=data)
        json_data = json.dumps(res.data, ensure_ascii=False)
        register_logger.error(f'请求：{current_url},返回参数为空')
        return json_data

    #执行核心算法语句，对信息存入表中
    SQL=sql()
    sql_operation=f"insert into userdata(avatar,avatarDesc,nickname,phone,status) values('{avatar}','{avatarDesc}','{nickname}','{phone}','{status}');"
    register_logger.info(f'正在执行数据库操作:{sql_operation}')
    try:
        detail_info,result = SQL.fetch_one(sql_operation)
        register_logger.info(f'数据库操作:{sql_operation},performance:{detail_info}')
        res.update(msg=f"{result}", data=data,code=ResponseCode.SUCCESS)
        register_logger.info(f'数据库操作完成:{sql_operation}')
    except Exception as e:
        register_logger.error(f'数据库操作失败:{e}')
    json_data = json.dumps(res.data, ensure_ascii=False)

    return json_data
















