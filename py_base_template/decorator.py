import logging
from functools import wraps
from typing import Union

from django.http import HttpRequest
from rest_framework import status
from rest_framework.request import Request

"""
自定义装饰 记录views 响应结果
"""

logger = logging.getLogger('full_logger')


def log_resp(func):
    """
    记录接口响应数据:
        1. 记录views文件响应数据日志
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        if isinstance(args[0], Union[Request, HttpRequest]):
            # 获取请求头 user-name
            # 注意的是header
            # key必须增加前缀HTTP，同时大写，例如你的key为username，那么应该写成：request.META.get("HTTP_USERNAME")
            # 另外就是当你的header中带有中横线，那么自动会被转成下划线，例如my - user的写成： request.META.get("HTTP_MY_USER")
            name = args[0].META.get("HTTP_USER_NAME")
            logger.info(f"user_info:{name}")
        if args[0].query_params:
            logger.info(f"query_params:{args[0].query_params}")
        if args[0].data:
            logger.info(f"query_params:{args[0].data}")
        res = func(self, *args, **kwargs)
        if res.status_code == status.HTTP_200_OK:
            logger.info("url execution [{}]{}complete,status_code:{},message:{}".format(
                func.__name__.upper(),
                args[0].path_info,
                res.status_code,
                # res.get('data') 或者 res.data['message'] 拿数据
                'success' if res.get('data') else res.data['results']
            ))
        else:
            logger.info("url execution [{}]{}fail,status_code:{},message:{}".format(
                func.__name__.upper(),
                args[0].path_info,
                res.status_code,
                # res.get('details') 拿数据
                res.get('details')
            ))
        return res

    return wrapper
