from django.urls import re_path

from apps.permission.views import PermissionViews
from apps.remote_file.views import RemoteViews

urlpatterns = [
    # 根据用户id 查询用户信息
    re_path(r'^remote/$', RemoteViews.as_view()),


]
