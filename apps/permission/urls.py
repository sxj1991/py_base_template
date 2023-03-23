from django.urls import re_path

from apps.permission.views import PermissionViews

urlpatterns = [
    # 根据用户id 查询用户信息
    re_path(r'^crud/$', PermissionViews.as_view()),


]
