# 导入MiddlewareMixin模块
from datetime import datetime, timedelta

import jwt
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .utils import parse_payload


# 自定义的类一定要继承MiddlewareMixin
class LoginMiddle(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if "login" in request.path:
            return
        else:
            result = parse_payload(request.headers["Token"])
            if not result["status"]:
                raise AuthenticationFailed("认证未通过")
        # 响应前端 详细错误信息
        # try:
        #     raise AuthenticationFailed("认证未通过")
        # except AuthenticationFailed as e:
        #     return




    # def process_response(self, request, response):
    #     print(f'login_response====process_response:{response}')
    #     return response



