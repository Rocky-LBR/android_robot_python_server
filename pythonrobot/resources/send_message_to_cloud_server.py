import requests
from pythonrobot.db import new_message


def send_message_to_cloud_server():
    data = new_message.select_IpNews_msg_code_all(msg_code="0")
    cloud_server_url=" "
    response = requests.get(cloud_server_url,data=data)
    if response.status_code==200:
        return {"msg":"message has been sent to cloud server,please wait msg"}
    else:
        return {"msg": "message has been sent to cloud server,please wait msg","error":response.status_code}
