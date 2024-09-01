import logging
from time import sleep
from pythonrobot.db import send_message
from pythonrobot.util.common import Logger
import requests


class SendRobotMessage():
    """
    对SendMessage表中状态为0的ip进行信息发送，
    """
    def __init__(self):
        self.type="send"
        self.content_type="text"
        self.content = ""
        self.nickname= ""
        self.data = {"type":self.type,"content_type":self.content_type,"content":self.content,"nickname":self.nickname}
        self.logger = Logger(name="server", level=logging.DEBUG)
        self.ip = "ip"
    def send_message(self):
        """
        1.从数据库中获取IP地址（0为需要发送，1为无需发送）及需要发送消息的的内容
        2.依次访问不同机器人前端，发送get内容
        3.前端收到指令后执行内容发送
        4.发送响应请求为200后，对数据库中已发送内容”send_status改为1，完成内容发送“
        :return:
        """
        #从数据库中获取需要发送信息的ip地址
        try:
            send_message.insert_SendMessage(ip="192.168.1.95:8080",send_msg="hello,nice to meet you",nickname="小智7",phone="+62 882-0161-78895",send_status="0")
            res = send_message.select_SendMessage_msg_code_all(send_status="0")
            if res:
                for res_content in res:
                    self.ip = res_content['ip']
                    self.data['content'] = res_content['send_msg']
                    self.data['nickname'] = res_content['phone']
                    url = f"http://{self.ip}/api/order"
                    try:
                        send_message.update_SendMessage(id=res_content["id"])
                        self.logger.info(f'msg has been sent')
                        responses = requests.post(url, data=self.data)
                        # if responses.status_code == 200:
                        #     # 发送完成后状态码修改为1
                        #     send_message.update_SendMessage(id=res_content["id"])
                        #     self.logger.info(f'msg has been sent')
                        # else:
                        #     self.logger.error(f'send msg error')
                    except Exception as e:
                        self.logger.error(f'send msg error')

            else:
                self.logger.info(f'no msg need to be sent')
                sleep(30)
        except Exception as e:
            self.logger.error(f'data read failed,msg:{e}')



if __name__=="__main__":
    A = SendRobotMessage()
    A.send_message()