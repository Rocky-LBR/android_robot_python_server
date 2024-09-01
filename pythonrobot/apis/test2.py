import json
from http.client import responses

from flask import Blueprint, request
from sqlalchemy.orm.sync import update

from ..util.util import ResMsg

ts2 = Blueprint("test2",__name__)



@ts2.route('/test/2',methods=['GET','POST'])
def test2():
    type_value = request.args.get('type')
    templist = ['status','user','talkList','conversation']
    res =ResMsg()
    print(type_value)
    if type_value in templist:
        update_data = {"data":[{
          "nickname": "+1 (458) 277-6000",
          "dateString": "2024/8/21",
          "content": "officia",
          "newMsgCount": 36
        },
        {
          "nickname": "+1 (458) 277-6000",
          "dateString": "2024/8/20",
          "content": "magna enim officia esse dolore",
          "newMsgCount": 77
        }
      ]}
    else:
        update_data={"data":["1"]}
    res.update(code=1,data=update_data["data"],msg="dolor commodo consequat reprehenderit")
    return res.data



from flask import Flask, request

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def my_api():
    type_param = request.args.get('type')  # 获取type的参数值
    return f'Type parameter value is: {type_param}'