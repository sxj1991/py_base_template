# 生成密钥接口
import time
from datetime import datetime, timedelta

import jwt
from jwt import exceptions

JWT_SALT = 'qazwsxpl@1!jwt'


def create_token(userName, timeout=24):
    """
        :param payload:  例如：{'user_id':1,'username':'lin'}用户信息
        :param timeout: token的过期时间，默认24小时
        :return:
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=timeout),  # 单位小时
        'iat': datetime.utcnow(),
        'data': {'username': userName}
    }

    token = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256")
    return token


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, key=JWT_SALT, verify=False, algorithms=['HS256'])
        result['status'] = True
        result['payload'] = verified_payload
        result['error'] = ''
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result
