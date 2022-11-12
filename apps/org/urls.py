from django.urls import re_path
from .views import OrgViews

urlpatterns = [
    # 根据用户id 查询用户信息
    re_path(r'^org/(?P<id>\d)/$', OrgViews.as_view()),

]
