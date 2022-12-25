from django.urls import re_path
from .views import OrgViews, FileViews

urlpatterns = [
    # 根据用户id 查询用户信息
    re_path(r'^info/(?P<id>\d)/$', OrgViews.as_view()),

    re_path(r'^file/$', FileViews.as_view()),

]
