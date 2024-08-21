import pymysql
from dbutils.pooled_db import PooledDB

#responseCode变量
class ResponseCode(object):
    SUCCESS = 0 #成功
    FAIL = -1 #失败
    NO_RESOURCE_FOUND = 40001 #未找到资源
    INVALID_PARAMETER = 40002 #参数无效
    ACCOUNT_OR_PASS_WORD_ERR = 40003 #账号或密码错误


#responseMessage提示
class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL = "失败"
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
        conn = self.POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return f"data has been registered."


