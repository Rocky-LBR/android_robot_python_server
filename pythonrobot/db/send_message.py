from sqlalchemy import Column, Integer, String, create_engine, func, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()

class SendMessage(Base):
    __tablename__ = 'send_message'
    id = Column(Integer, autoincrement=True,
                primary_key=True, nullable=False)  # 自增、主键、不为空
    ip = Column(String(255), nullable=False)  # 字符串、不为空
    send_msg = Column(String(255), nullable=False)  # 字符串、不为空
    nickname = Column(String(500), nullable=False)  # 字符串、不为空
    phone = Column(String(500), nullable=False)  # 字符串、不为空
    send_status = Column(String(255), nullable=False)  # 字符串、不为空


engine = create_engine(f'mysql+pymysql://root:123456@38.6.220.83:3306/mydatabase')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

#获取需要发送消息的所有数据
def select_SendMessage_msg_code_all(send_status):
    # 获取多条，只返回第一条
    res = session.query(SendMessage).filter(SendMessage.send_status == send_status).all()
    session.commit()
    json_data = [result_to_dict(result) for result in res]
    return json_data

def select_SendMessage_ip_all():
    res = session.query(SendMessage).all()
    json_data = [to_dict(ip) for ip in res]
    return json_data

def insert_SendMessage(ip, send_msg,nickname,phone,send_status):
    # 创建新对象:
    News=SendMessage(ip=ip, send_msg=send_msg,nickname=nickname,phone=phone,send_status=send_status)
    session.add(News)
    # 提交即保存到数据库
    session.commit()
    # 判断是否插入成功
    session.close()
def update_SendMessage(id):
    # 假设要更新 id 为 1 的消息
    message = session.query(SendMessage).filter_by(id=id).first()
    if message:
        message.send_status = '1'  # 修改 send_status 的值
        session.commit()  # 提交更改

def to_dict(result):
    return {
            'id': result.id,
            'ip': result.ip
        }

def result_to_dict(result):
    return {
        'id':result.id,
        'ip': result.ip,
        'send_msg': result.send_msg,
        'nickname':result.nickname,
        'phone':result.phone,
        'send_status':result.send_status,
    }

