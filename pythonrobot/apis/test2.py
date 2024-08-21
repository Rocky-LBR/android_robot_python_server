import json

from flask import Blueprint

from pythonrobot.util.util import ResMsg

ts2 = Blueprint("test2",__name__)



@ts2.route('/test/2',methods=['GET','POST'])
def test2():
    res = ResMsg()
    data = json.dumps(res.data,ensure_ascii=False)
    print(f"{data}正在调用该接口")
    return data
