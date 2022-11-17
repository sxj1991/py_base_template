# 导入MiddlewareMixin模块
import json
from datetime import datetime, timedelta
from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from py_base_template import cache
from .utils import parse_payload
import logging

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "HEAD,OPTIONS",
    "Access-Control-Allow-Credentials": "true",
}

# 自定义的类一定要继承MiddlewareMixin
logger = logging.getLogger('full_logger')


class LoginMiddle(MiddlewareMixin):
    @staticmethod
    def build_cors_resp(http_origin, details, method, code=status.HTTP_400_BAD_REQUEST):
        resp = HttpResponse(
            json.dumps({
                "message": "fail",
                "details": details,
            }),
            status=code,
            content_type="application/json",
        )
        header = CORS_HEADERS.copy()
        resp.__setitem__(
            "Access-Control-Allow-Methods", header["Access-Control-Allow-Methods"] + f",{method}"
        )
        resp.__setitem__("Access-Control-Allow-Origin", http_origin)
        resp.__setitem__("Access-Control-Allow-Credentials", "true")
        return resp

    def process_request(self, request: HttpRequest):
        if "login" in request.path:
            return
        else:
            token = request.META.get("HTTP_TOKEN")
            # 判断缓存是否再存key key不存在则过期
            if not cache.exist_cache(token):
                try:
                    logger.error("token过期")
                    raise AuthenticationFailed("token过期")
                except AuthenticationFailed as e:
                    return self.build_cors_resp("*", str(e), request.method, status.HTTP_401_UNAUTHORIZED)
            # 刷新token 缓存时间
            cache.refresh_cache(token, token)
            # 验证token
            result = parse_payload(token)
            if not result["status"]:
                # 响应前端 详细错误信息
                try:
                    logger.error("认证未通过")
                    raise AuthenticationFailed("认证未通过")
                except AuthenticationFailed as e:
                    return self.build_cors_resp("*", str(e), request.method, status.HTTP_401_UNAUTHORIZED)


    # 响应数据中间件拦截
    # def process_response(self, request, response):
    #     print(f'login_response====process_response:{response}')
    #     return response
