import time
from flask import Blueprint, request,current_app
from pythonrobot.db.send_message import SendMessage
from pythonrobot.util.config import dir_path
from pythonrobot.util.util import log_performance

ls = Blueprint("local_server",__name__)


#请求前执行性能监视
@ls.before_request
def start_timer():
    request.start_time = time.time()

@ls.after_request
def log_request(res):
    log_performance(res)
    return res


@ls.route('/local_server',methods=['POST'])
def local_server():
    """
    提供云服务访问，用于接收数据，保存到云端
    需要根据云接口来进行字段调整
    """
    try:
        request_json = request.json
        if request_json:
            id = request_json.get('id', None)
            send_msg = request_json.get('send_msg', None)
            ip = request_json.get('ip', None)
            phone = request_json.get('phone', None)
            nickname = request_json.get('nickname',None)
            # 数据库操作把数据按照ip、data、time、msgcode写入数据库
            SendMessage.insert_send_message(ip=ip, send_msg=send_msg,nickname=nickname,phone=phone,send_status="0")
            current_app.logger.info(f"msg had been recept")
            return {"code": 200, "msg": "success"}
        else:
            return {'error': "Please provide correct info "}
    except Exception as e:
        return {'error': e}, 400

#尚未对图片进行数据库写入操作
@ls.route('/local_picture_server',methods=['POST'])
def local_picture_server():
    try:
        pic_path = dir_path / 'data' / 'robot_api.jpg'
        current_app.logger.info("data has been load")
        file_path =pic_path
        file = request.files['file']
        file.save(file_path)
        return {'code': 200, "msg": "success"}
    except Exception as e:
        return {'code': 400, "msg": "failed"}