from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserView, LoginView, UsersView


urlpatterns = [
    # 根据用户id 查询用户信息
    re_path(r'^info/(?P<id>\d)/$', UserView.as_view()),
    # 用户信息
    re_path(r'^infos/$', UsersView.as_view()),
    # 用户登录 获取token
    re_path(r'^login/$', LoginView.as_view()),
]
