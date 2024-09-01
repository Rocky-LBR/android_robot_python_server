import logging

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from pythonrobot.db import send_message
from pythonrobot.util.common import Logger

type = "send"
content_type = "text"
content = ""
nickname = ""
data = {"type": type, "content_type": content_type, "content": content, "nickname": nickname}
logger = Logger(name="server", level=logging.DEBUG)
ip = "ip"

for i in range(5):
    send_message.insert_SendMessage(ip="192.168.1.95:8080", send_msg="hello,nice to meet you", nickname="小智7",
                                phone="+62 882-0161-78895", send_status="0")

res = send_message.select_SendMessage_msg_code_all(send_status="0")
print(res)

# 定义要调用的 POST 请求函数
def make_post_request(res_content):
    print(res_content)
    ip = res_content['ip']
    data['content'] = res_content['send_msg']
    data['nickname'] = res_content['phone']
    url = f"http://{ip}/api/order"
    try:
        send_message.update_SendMessage(id=res_content["id"])
        logger.info(f'msg has been sent')
        # responses = requests.post(url, json=self.data)
        # if responses.status_code == 200:
        #     # 发送完成后状态码修改为1
        #     send_message.update_SendMessage(id=res_content["id"])
        #     self.logger.info(f'msg has been sent')
        # else:
        #     self.logger.error(f'send msg error')
    except Exception as e:
        # 测试模拟失败时修改为1
        logger.error(f'send msg error')
    return

def Th(res):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 创建未来对象
        future_to_info = {executor.submit(make_post_request, info): info for info in res}

        # 处理已完成的请求
        for future in as_completed(future_to_info):
            info = future_to_info[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Successfully posted data: {info['data']} to {info['url']}, response: {result}")
            except Exception as e:
                print(f"Failed to post data: {info['data']} to {info['url']}, error: {e}")

    print("All requests completed.")


make_post_request(res)