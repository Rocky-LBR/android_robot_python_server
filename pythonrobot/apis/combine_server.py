import json
import time
from flask import Blueprint, Flask, jsonify, request, current_app

from pythonrobot.util.util import log_performance, combine_api, ResMsg, ResponseCode

cs = Blueprint("combine_server",__name__)


#请求前执行性能监视(尚未完成)
@cs.before_request
def start_timer():
    request.start_time = time.time()

@cs.after_request
def log_request(res):
    log_performance(res)
    return res

#聚合服务接口，对请求进行聚合处理，返回多个请求的json参数
@cs.route('/combine_server',methods=['GET','POST'])
def combine_server():
    res = ResMsg()
    api_dict_info = {}
    api1 = "http://127.0.0.1:5000/test/1"
    api2 = "http://127.0.0.1:5000/test/2"
    api_list = [api1,api2]
    for api in api_list:
        if api not in api_dict_info.keys():
            api_dict_info[api] = ""
    current_app.logger.info("开始进行聚合请求")
    try:
        aggregated_data = combine_api(api_dict_info)
        current_app.logger.info("完成聚合请求")
        res.update(data=aggregated_data,code=ResponseCode.SUCCESS)
        data =json.dumps(res.data, ensure_ascii=False)
        return data
    except Exception as e:
        current_app.logger.error(f"聚合错误:{e}")
        res.update(data=e,code=ResponseCode.FAIL)
        data = json.dumps(res.data, ensure_ascii=False)
        return data






