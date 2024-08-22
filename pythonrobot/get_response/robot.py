
import requests
from flask import jsonify


#获取前端信息返回json列表
def get_robot_message(message_type):
    url = "/api/machine?type="
    templist = ['status','user','talkList','conversation']
    if message_type in templist:
        url=url+message_type
        response = requests.request("GET", url)
        data = response.json()
    return jsonify(data)

