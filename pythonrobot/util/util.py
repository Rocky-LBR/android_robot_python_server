import logging
import time
from logging.handlers import RotatingFileHandler

import psutil
import pymysql
import requests
from dbutils.pooled_db import PooledDB
from flask import request, Flask,current_app

from pythonrobot.util.config import dir_path

#responseCode变量
class ResponseCode(object):
    SUCCESS = True #成功
    FAIL = False #失败

#responseMessage提示
class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL = "服务器内部错误"
    NO_RESOURCE_FOUND =  "未找到资源"
    INVALID_PARAMETER =  "参数无效"
    ACCOUNT_OR_PASS_WORD_ERR = "账号或密码错误"

#响应逻辑
class ResMsg(object):
    """
    封装响应文本
    """
    def __init__(self, data=None, code=ResponseCode.SUCCESS,
    			 msg=ResponseMessage.SUCCESS):
        self._data = data
        self._msg = msg
        self._code = code

    def update(self, code=None, data=None, msg=None):
        """
        更新默认响应文本
        :param code:响应状态码
        :param data: 响应数据
        :param msg: 响应消息
        :return:
        """
        if code is not None:
            self._code = code
        if data is not None:
            self._data = data
        if msg is not None:
            self._msg = msg

    def add_field(self, name=None, value=None):
        """
        在响应文本中加入新的字段，方便使用
        :param name: 变量名
        :param value: 变量值
        :return:
        """
        if name is not None and value is not None:
            self.__dict__[name] = value

    @property
    def data(self):
        """
        输出响应文本内容
        :return:
        """
        body = self.__dict__
        body["data"] = body.pop("_data")
        body["msg"] = body.pop("_msg")
        body["code"] = body.pop("_code")
        return body

#基于线程池对数据库进行访问
class sql:
    def __init__(self):
        self.POOL = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=1,
            maxcached=3,
            blocking=True,#是否进行阻塞
            setsession=[],
            ping=0,
            host='127.0.0.1', port=3306, user='root', password='123456', db='user'
        )

    def fetch_one(self,sql):
        """
        sql为数据库操作语句
        :param sql:
        :return:
        """
        # 使用连接池进行连接
        start_time = time.time()
        conn = self.POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        end_time = time.time()
        duration = end_time-start_time
        cpu_percent = psutil.cpu_percent()  # 获取CPU使用率
        memory_info = psutil.virtual_memory()  # 获取内存信息
        detail_info = {"time":f"{duration:.2f}","cpu":cpu_percent,"memory_cpu":memory_info.percent}
        return detail_info,f"data has been registered."

# #配置日志
# def cls_log():
#     import logging
#
#     # 配置日志记录器
#     # logger = logging.getLogger('flask_app')
#     # logger.setLevel(logging.INFO)
#
#     # 配置自定义日志记录器，用于自己需要调试的信息展示
#     flask_logger = logging.getLogger()
#     flask_logger.setLevel(logging.INFO)  # 设置日志输出等级至少在INFO及以上
#
#     # 创建一个文件处理器，将日志记录到flask_api.log文件中
#     log_file_path = dir_path / 'log' / 'robot_api.log'  # 使用 / 运算符拼接路径
#     file_handler = logging.FileHandler(log_file_path)
#     file_handler.setLevel(logging.INFO)
#
#     # 创建一个控制台处理器，将日志输出到控制台
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)  # 设置日志输出等级至少在INFO及以上
#
#     # 定义日志格式
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#
#     # 将处理器添加到日志记录器
#     flask_logger.addHandler(file_handler)  # 将自定义的日志写入文件中
#     flask_logger.addHandler(console_handler)  # 将自定义的日志写输出到控制台中
#
#     return flask_logger

#配置日志
def register_log(app: Flask):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_path = dir_path / 'log' / 'robot_api.log'  # 使用 / 运算符拼接路径
    file_handler = RotatingFileHandler(log_file_path,maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


#记录cpu、性能、内存状态
def log_performance(res):
    current_url = request.url
    duration = time.time() - request.start_time # 获取请求消耗时间
    cpu_percent = psutil.cpu_percent()  # 获取CPU使用率
    memory_info = psutil.virtual_memory()  # 获取内存信息
    current_app.logger.info(f"Request to {current_url} took {duration:.2f} seconds,CPU:{cpu_percent},memory_info{memory_info.percent}")

#聚合多个请求的参数
def combine_api(api_dict):
    for api in api_dict:
        try:
            response = requests.get(api)
            current_app.logger.info(f"正在聚合{api},状态码为：{response.status_code}")
            api_dict[api]=response.json() if response.status_code == 200 else None
        except Exception as e:
            current_app.logger.error(f"聚合{api}失败,状态码为：{response.status_code},error:{e}")
    return api_dict

#清除日志
def clear_log():
    log_file_path = dir_path / 'log' / 'robot_api.log'  # 使用 / 运算符拼接路径
    filename = log_file_path
    with open(filename, 'w') as file:
        pass

#清楚数据库数据
def clear_mysql():
    pass




if __name__ =="__main__":
    clear_log()