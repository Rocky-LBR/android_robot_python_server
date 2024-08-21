import json
import time

from flask import Blueprint, jsonify
import requests


from pythonrobot.util.util import ResMsg

cls = Blueprint("cloud_server",__name__)

#用户进行注册后，每5s访问外部url（云服务器）
@cls.route('/cloud_server',methods=['GET','POST'])
def cloud_server():
    """
    external_api_url:云服务器接口
    :return:
    """
    external_api_url = "http://127.0.0.1:5000/test1"
    res = ResMsg()
    while True:
        try:
            time.sleep(5)
            response = requests.get(external_api_url)
            if response.status_code == 200:
                data = response.json()  # 假设返回的是 JSON 格式数据
                #传递参数给到前端api
                result = requests.post("http://127.0.0.1:5000/test1",json=data)

        except requests.exceptions.RequestException as e:
            return json.dumps(res.data(msg=e))