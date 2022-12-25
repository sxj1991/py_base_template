from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView

from py_base_template import cache
from py_base_template.base_paginator import PageMixin
from py_base_template.decorator import log_resp
from .serializers import UserSerializer
from .models import UserModel, DetailModel
from apps.base_response.api_response import APIResponse
from .utils import create_token
import logging

# Create your views here.
logger = logging.getLogger('full_logger')


class UserView(APIView):
    # authentication_classes = [JwtAuthentication, ] 局部认证器设置

    @log_resp
    def get(self, request, id):
        # 获取认证标记
        if request.auth:
            logger.info(msg=f"接收前端查询数据:request:{request}-id:{id}")
            user = UserModel.objects.filter(user_id=id).first()
            if user:
                serializer = UserSerializer(instance=user)
                return APIResponse(results=serializer.data)
        return APIResponse(data_msg="认证不通过", data_status="5002", http_status=status.HTTP_204_NO_CONTENT)


# 引入事务管理
class UsersView(APIView):

    def get(self, request):
        users = UserModel.objects.all().order_by("-create_time")
        if users:
            # model 序列化几种方式：
            # 1. model 手动转字典类型 user.to_dict()
            new_user = [user.to_dict() for user in users]
            # 2. 利用序列化器
            serializer = UserSerializer(instance=users, many=True)
            # 3. 利用序列化器基础上 添加分页操作
            data = PageMixin.build_base_paginator(request, users, UserSerializer)
            return APIResponse(results=data)
        return APIResponse(data_msg="数据不存在", data_status="5002", http_status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # 用户名唯一
        name = request.data["userName"]
        if name:
            user = UserModel.objects.filter(user_name=name)
            if user:
                return APIResponse(data_msg="", data_status="5001")
            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    # 代码块级 事务 非代码块内 则不会放入事务
                    with transaction.atomic():
                        serializer.save()
                        transaction.on_commit(lambda: logger.info("事务成功提交回滚方法"))
                    return APIResponse()
                else:
                    return APIResponse(data_msg="", results=serializer.errors, data_status="5001")
        return APIResponse(data_msg="参数不存在", data_status="5001", http_status=status.HTTP_204_NO_CONTENT)

    # 函数级的事务控制
    @transaction.atomic
    def put(self, request):
        user = UserModel.objects.get(user_id=request.data["userId"] or "")
        serializer = UserSerializer(data=request.data, instance=user)
        # 回滚保存点
        save_tag = transaction.savepoint()
        try:
            if serializer.is_valid():
                serializer.save()
                return APIResponse()
        except:
            # 回滚操作
            transaction.savepoint_rollback(save_tag)

        return APIResponse(data_msg="认证不通过", results=serializer.errors, data_status="5001")

    def delete(self, request):
        userId = request.data["userId"]
        if userId:
            UserModel.objects.get(user_id=userId).delete()
            DetailModel.objects.filter(user_id=userId).delete()
            return APIResponse()

        return APIResponse(data_msg="", data_status="5001")


class LoginView(APIView):

    def post(self, request):
        # 用户名唯一
        name = request.data["userName"]
        if name:
            user = UserModel.objects.filter(user_name=name).first()
            if user:
                password = request.data["password"]
                if password and password == user.password:
                    # 返回token
                    token = create_token(userId=user.user_id)
                    cache.write_data_to_cache(key=token, value=token)
                    return APIResponse(results=token)
        return APIResponse(data_msg="", http_status=status.HTTP_401_UNAUTHORIZED)
