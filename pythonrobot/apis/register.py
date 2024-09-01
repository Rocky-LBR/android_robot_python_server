
import time

from flask import Blueprint, request, current_app

from ..db import user, new_message
from ..util.util import ResMsg, ResponseMessage,log_performance, ResponseCode

rs = Blueprint("register",__name__)


#请求前执行性能监视
@rs.before_request
def start_timer():
    request.start_time = time.time()

@rs.after_request
def log_request(res):
    log_performance(res)
    return res


@rs.route('/api/register',methods=['POST'])
def register():
    """
       {
    "avatar": "string",
    "avatarDesc": "string",
    "nickname": "string",
    "status": "string",
    "phone": "string"
        }
       """
    #获取用户请求信息
    current_url = request.url
    data = request.get_json()
    #响应data数据为空，返回参数不正确，状态码Flase
    if not data:
        current_app.logger.error(f'data：{current_url},msg：返回参数为空')
        return {"code":False,"msg":"parameters is null","url":current_url}
    #执行核心算法语句，对信息存入表中，数据库采用orm进行操作
    try:
        request_data = request.json
        current_app.logger.info(f"request.json', {request.json}")
        #查询数据库中是否已经存在该手机的用户
        exists_data = user.select_user_phone(phone=request_data['phone'],ip=request_data["ip"])
        if exists_data:
            current_app.logger.error({"code":False,"msg":"fail","data":"the phone has been registered already"})
            return {"code":False,"msg":"fail","data":"the phone has been registered already"}
        # 数据库插入数据
        else:
            result = user.insert_user(request_data["avatar"], request_data["avatarDesc"], request_data["nickname"],
                                      request_data["status"], request_data["phone"],request_data["ip"])
            #  判断是否插入成功
            if result == True:
                current_app.logger.info({"code":True,"msg":"success","data":"the phone has been registered successfully"})
                return {"code":True,"msg":"success","data":"the phone has been registered successfully"}
            else:
                current_app.logger.info({"code":False, "msg":"fail", "data":"data registered fail"})
                return {"code":False, "msg":"fail", "data":"data registered fail"}
    except Exception as e:
        current_app.logger.error(e)
        return e














