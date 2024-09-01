import http.client
import json
import logging
from pythonrobot.db import user,new_message
from pythonrobot.util.common import Logger


class TempList(object):
    USER = 'user'  # 成功
    TALKLIST = 'talkList'
    CONVERSATION = 'conversation'# 失败
class TalkList(object):
    NICKNAME='nickname'
    DATESTRING='dateString'
    CONTENE='content'
    NEWMSGCOUNT='newMsgCount'
class UserList(object):
    AVATAR = "avatar"
    AVARARDESC ="avatarDesc"
    NICKNAME = "nickname"
    PHONE = "phone"
    STATUS = "status"


logger =Logger(name="server",level=logging.DEBUG)
#根据数据库中的ip地址信息获取前端机器人的信息
def get_robot_message():
    """
    从数据库中获取所有ip地址，根据ip地址请求安卓机器人，获取机器人是否有最新消息
    :return:
    """
    #从数据库中获取ip地址，对ip地址进行逐个请求，获取每个ip地址的信息(获取失败如何处理？)
    try:
        ip_group=user.select_user_ip(value='0')
        if ip_group:
            logger.info('ip user has been read')
        else:
            logger.info('no message need to be send')
    except Exception as e:
        logger.error('select failed')
        return {"msg": 'server error', 'code': 402}
    try:
        all_response={}
        for ip in ip_group:
            for i in ip.keys():
                ip = ip[i]
            responses = {}
            templist_temp = [TempList.USER, TempList.TALKLIST]
            conn = http.client.HTTPSConnection("apifoxmock.com")
            payload =json.dumps({})
            for type_name in templist_temp:
                conn.request("POST", f"/m1/5025950-4685935-default/api/machine?type={type_name}", payload)
                res = conn.getresponse()
                if res.status == 200:
                    # 将成功的响应数据写入到数据库中（ip,msg_code,msg）
                    if type_name not in responses:
                        responses[type_name]=res.read().decode("utf-8")
                else:
                    logger.error(f'request failed')
            get_talkList(responses,ip)
            if ip not in all_response:
                all_response[ip] = responses
    except Exception as e:
        return {"msg":'the api are failed to','code':402}

#执行数据库写入操作
def get_talkList(data,ip):
    try:
        data_load = json.loads(data[TempList.USER])
        #获取用户信息
        user = data_load["data"]
        phone = data_load["data"][UserList.PHONE]
        data_load = json.loads(data[TempList.TALKLIST])
        talklist = data_load["data"]
        for item in data_load["data"]:
            nickname = item[TalkList.NICKNAME]
            msg_code = item[TalkList.NEWMSGCOUNT]
            conversation_group,msg = get_conversation()
            # 判断该数据是否已经写入数据库
            exist_data =new_message.select_NewMessage_by_msg_and_ip(msg=msg,ip=ip)
            if not exist_data:
                res = new_message.insert_NewMessage(ip=ip, msg_code=msg_code, msg=msg,nickname=nickname,phone=phone,msg_status="0",user=user,talklist=talklist,conversation=conversation_group)
                if res:
                    logger.info('data has been wrote in db')
            else:
                logger.info('data has been wrote already')
    except Exception as e:
        return {"msg":'data operated failed','code':402}

#根据会话角色、msg_code获取会话具体内容,需根据接口字段进行更改
def get_conversation():
    try:
        conversation=""
        conn = http.client.HTTPSConnection("apifoxmock.com")
        payload = ''
        conn.request("POST", f"/m1/5025950-4685935-default/api/machine?type=conversation", payload)
        res = conn.getresponse()
        json_data=json.loads(res.read().decode('utf-8'))
        conversation_group = json_data['data']
        for item  in json_data['data']:
            conversation+= item['msg']
            conversation += ";"
        return conversation_group,conversation
    except Exception as e:
        logger.error(f'conversation read faile msg{e}')
        return {"msg":'data operated failed','code':402}





if __name__ =="__main__":
    get_robot_message()

