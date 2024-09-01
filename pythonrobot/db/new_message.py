import uuid
from sqlalchemy import Column, Integer, String, create_engine, func, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.coercions import expect

Base = declarative_base()

class NewMessage(Base):
    __tablename__ = 'new_message'
    id = Column(Integer, autoincrement=True,
                primary_key=True, nullable=False)  # 自增、主键、不为空
    ip = Column(String(255), nullable=False)
    msg_code = Column(String(255), nullable=False)
    msg = Column(String(255), nullable=False)
    nickname = Column(String(500), nullable=False)
    phone = Column(String(500), nullable=False)
    msg_status = Column(String(255))
    session_id = Column(String(255))
    user = Column(String(255))
    status = Column(String(255))
    talklist = Column(String(255))
    conversation = Column(String(255))

# 初始化数据库连接:
engine = create_engine(f'mysql+pymysql://root:123456@38.6.220.83:3306/mydatabase')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

#获取需要发送消息的所有数据
def select_IpNews_msg_code_all(msg_code):
    # 获取多条，只返回第一条
    res = session.query(NewMessage).filter(NewMessage.msg_code == msg_code).all()
    session.commit()
    json_data = [result_to_dict(result) for result in res]
    return json_data

#对数据库进行插入操作
def insert_NewMessage(ip, msg_code,msg,nickname,phone,msg_status,user,talklist,conversation):
    # 创建新对象:
    # try:
    News=NewMessage(ip=ip, msg_code=msg_code, msg=msg,nickname=nickname,phone=phone,msg_status=msg_status,user=user,talklist=talklist,conversation=conversation)
    # 添加到session
    session.add(News)
    # 提交即保存到数据库
    try:
        session.commit()
    except Exception as e:
        print('data insert failed')
    result = [result_to_dict(result) for result in News]
    session.close()
    return result


def select_NewMessage_by_msg_and_ip(msg,ip):
    try:
        res = session.query(NewMessage).filter(NewMessage.msg == msg,NewMessage.ip==ip).all()
        session.commit()
        result = [result_to_dict(result) for result in res]
        return result
    except Exception as e:
        return None
        # return {"msg":"select data failed"}


def select_IpNews_ip_all():
    res = session.query(NewMessage).all()
    json_data = [to_dict(ip) for ip in res]
    return json_data

def to_dict(result):
    return {
            'id': result.id,
            'ip': result.ip
        }

def result_to_dict(result):
    return {
        'id': result.id,
        'msg_code': result.msg_code,
        'ip':result.ip,
        'nickname':result.nickname,
        'phone':result.phone,
        'msg':result.msg,
        "msg_status":result.msg_status
    }

