from rest_framework.permissions import BasePermission

from apps.login.models import UserModel


# 全局权限校验
class global_permission(BasePermission):
    """
    自定义权限，可用于全局配置，也可以用于局部
    """

    def has_permission(self, request, view):
        """
        视图权限
        返回结果未True则表示允许访问视图类
        request: 本次客户端提交的请求对象
        view: 本次客户端访问的视图类
        """
        if "login" in request.path:
            return True
        # request.auth 通过auth.py 存入认证的用户信息
        # TODO RBAC权限设计模型实现权限设计
        UserModel.objects.filter(user_name=request.auth).first()

        return True

    def has_object_permission(self, request, view, obj):
        """
        模型权限
        返回结果为True则表示允许操作模型对象
        """
        return True
