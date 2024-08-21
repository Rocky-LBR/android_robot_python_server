import pymysql
from flask import Blueprint,Flask, jsonify
import requests
from sqlalchemy.sql.functions import aggregate_strings

cs = Blueprint("combine_server",__name__)


def combine_api(api_dict):
    for api in api_dict:
        response = requests.get(api)
        api_dict[api]=response.json() if response.status_code == 200 else None
    return api_dict


#聚合服务接口，对请求进行聚合处理，返回多个请求的json参数
@cs.route('/combine_server',methods=['GET','POST'])
def combine_server():
    api_dict_info = {}
    api1 = "http://127.0.0.1:5000/test/1"
    api2 = "http://127.0.0.1:5000/test/2"
    api_list = [api1,api2]
    for api in api_list:
        if api not in api_dict_info.keys():
            api_dict_info[api] = ""
    aggregated_data = combine_api(api_dict_info)
    return jsonify(aggregated_data)




