import json

from flask import Blueprint

from pythonrobot.util.util import ResMsg

ts1 = Blueprint("test1",__name__)

@ts1.route('/test/1',methods=['GET','POST'])
def test1():
    res = ResMsg()
    data = json.dumps(res.data,ensure_ascii=False)
    return data



