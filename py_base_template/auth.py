from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
import logging

from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.login.models import UserModel
from apps.login.utils import parse_payload

logger = logging.getLogger('full_logger')


# 全局认证类
class JwtAuthentication(BaseAuthentication):
    """
    自定义认证方式
    """

    def authenticate(self, request):
        """
        认证方法
        request: 本次客户端发送过来的http请求对象
        """
        if "login" in request.path:
            return
        token = request.META.get("HTTP_TOKEN")
        result = parse_payload(token)
        logger.info(f'user:{result}')
        if not result["status"]:
            # 响应前端 详细错误信息
            logger.error("认证未通过")
            raise AuthenticationFailed("认证未通过")
        # 获取当前系统中用户表对应的用户模型类
        userId = result['payload']['data']['userId']
        user = UserModel.objects.filter(user_id=userId).first()
        # 放入认证的模型和认证的标记
        return (user, user.user_id)
