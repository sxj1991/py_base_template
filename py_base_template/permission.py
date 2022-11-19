from rest_framework.permissions import BasePermission

from apps.login.models import UserModel


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
        u = UserModel.objects.filter(user_name=request.auth).first()

        return u.role == "admin"

    def has_object_permission(self, request, view, obj):
        """
        模型权限
        返回结果为True则表示允许操作模型对象
        """
        return True
