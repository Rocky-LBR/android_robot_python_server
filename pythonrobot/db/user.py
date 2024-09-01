import uuid

from sqlalchemy import Column, Integer, String, create_engine, func, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(Integer, autoincrement=True,
                primary_key=True, nullable=False)  # 自增、主键、不为空
    avatar = Column(String(100), nullable=False)  # 字符串、不为空
    avatarDesc = Column(String(500), nullable=False)  # 字符串、不为空
    nickname = Column(String(100), nullable=False)  # 字符串、不为空
    status = Column(String(500), nullable=False)  # 字符串、不为空
    phone = Column(String(500), nullable=False)  # 字符串、不为空
    ip = Column(String(500), nullable=False)  # 字符串、不为空


engine = create_engine(f'mysql+pymysql://root:123456@38.6.220.83:3306/mydatabase')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


def insert_user(avatar, avatarDesc, nickname,status,phone,ip):
    # 创建新User对象:
    user=User(avatar=avatar,avatarDesc=avatarDesc,nickname=nickname,status=status,phone=phone,ip=ip)# 插入数据表成功后，返回的是一个对象，具有id属性
    # 添加到session
    session.add(user)
    # 提交即保存到数据库
    session.commit()
    # 判断是否插入成功
    if user.id:
        return True
    else:
        return False

#根据字段名进行参数选择
def select_user_phone(phone,ip):
    res = session.query(User).filter(User.phone == phone,User.ip ==ip).all()
    session.commit()
    json_data = [result_to_dict(result) for result in res]
    session.close()
    return json_data

def select_user_ip(value):
    res = session.query(User).filter(User.status == value).all()
    session.commit()
    json_data = [result_to_dict(result) for result in res]
    return json_data


def result_to_dict(result):
    return {
        result.id:result.ip
    }