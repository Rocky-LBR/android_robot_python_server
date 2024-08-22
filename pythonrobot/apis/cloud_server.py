import json
import time
from flask import Blueprint, request
import requests
from pythonrobot.util.util import ResMsg, cls_log, log_performance
cls = Blueprint("cloud_server",__name__)


#请求前执行性能监视
@cls.before_request
def start_timer():
    request.start_time = time.time()

# @cls.after_request
# def log_request(cloud_server_logger):
#     log_performance(cloud_server_logger)
#     return


#用户进行注册后，每5s访问外部url（云服务器）
@cls.route('/cloud_server',methods=['GET','POST'])
def cloud_server():
    """
    external_api_url:云服务器接口
    :return:
    """
    cloud_server_logger = cls_log()
    external_api_url = "http://127.0.0.1:5000/test/1"
    res = ResMsg()
    api_time = 0
    while api_time <=0:
        try:
            time.sleep(5)
            api_time +=5
            cloud_server_logger.info(f"正在开始访问云服务{external_api_url}")
            response = requests.get(external_api_url)
            cloud_server_logger.info(f"访问云服务{external_api_url}完成,状态码为{response.status_code}")
            if response.status_code != 200:
                cloud_server_logger.error(f"访问云服务{external_api_url}失败,状态码为{response.status_code}")
                break
            try:
                cloud_server_logger.info(f"开始json化{external_api_url}响应数据")
                data = response.json()  # 假设返回的是 JSON 格式数据
                cloud_server_logger.info(f"json化{external_api_url}响应数据完成")
            except Exception as e:
                cloud_server_logger.error(f"json化{external_api_url}响应数据失败，失败原因为{e}")
        except Exception as e:
            return json.dumps(res.data(msg=e))
    return json.dumps(res.data)