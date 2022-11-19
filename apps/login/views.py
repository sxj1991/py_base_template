from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from py_base_template import cache
from py_base_template.auth import JwtAuthentication
from py_base_template.base_paginator import PageMixin
from py_base_template.decorator import log_resp
from py_base_template.exception import global_exception_handler
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


class UsersView(APIView):

    def get(self, request):
        users = UserModel.objects.all()
        if users:
            serializer = UserSerializer(instance=users, many=True)
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
                    serializer.save()
                    return APIResponse()
                else:
                    return APIResponse(data_msg="", results=serializer.errors, data_status="5001")
        return APIResponse(data_msg="参数不存在", data_status="5001", http_status=status.HTTP_204_NO_CONTENT)

    def put(self, request):

        user = UserModel.objects.get(user_id=request.data["userId"] or "")
        serializer = UserSerializer(data=request.data, instance=user)

        if serializer.is_valid():
            serializer.save()
            return APIResponse()
        else:
            return APIResponse(data_msg="认证不通过", results=serializer.errors, data_status="5001")

    def delete(self, request, id):
        if id:
            UserModel.objects.get(user_id=id).delete()
            DetailModel.objects.filter(user_id=id).delete()
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
                    token = create_token(userName=user.user_name)
                    cache.write_data_to_cache(key=token, value=token)
                    return APIResponse(results=token)
        return APIResponse(data_msg="", http_status=status.HTTP_401_UNAUTHORIZED)
