import time

from pythonrobot.resources.get_robot_message import get_robot_message
from pythonrobot.resources.send_message_to_cloud_server import send_message_to_cloud_server
from pythonrobot.resources.send_robot_message import SendRobotMessage

if __name__ == "__main__":
    res = SendRobotMessage()
    while True:
        time.sleep(2)
        get_robot_message()
        send_message_to_cloud_server()
        res.send_message()