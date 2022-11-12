from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import UserModel, DetailModel
from apps.base_response.api_response import APIResponse
from .utils import create_token
import logging


# Create your views here.


class UserView(APIView):

    def get(self, request, id):
        logging.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}")
        user = UserModel.objects.filter(user_id=id).first()
        if user:
            serializer = UserSerializer(instance=user)
            return APIResponse(results=serializer.data)
        return APIResponse(data_msg=False, status="5002")


class UsersView(APIView):
    def get(self, request):
        users = UserModel.objects.all()
        if users:
            serializer = UserSerializer(instance=users, many=True)
            return APIResponse(results=serializer.data)
        return APIResponse(data_msg=False, status="5002")

    def post(self, request):
        # 用户名唯一
        name = request.data["userName"]
        if name:
            user = UserModel.objects.filter(user_name=name)
            if user:
                return APIResponse(data_msg=False, status="5001")
            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return APIResponse()
                else:
                    return APIResponse(data_msg=False, results=serializer.errors, status="5001")
        return APIResponse(data_msg=False, status="5001")

    def put(self, request):

        user = UserModel.objects.get(user_id=request.data["userId"] or "")
        serializer = UserSerializer(data=request.data, instance=user)

        if serializer.is_valid():
            serializer.save()
            return APIResponse()
        else:
            return APIResponse(data_msg=False, results=serializer.errors, status="5001")


    def delete(self, request, id):
        if id:
            UserModel.objects.get(user_id=id).delete()
            DetailModel.objects.filter(user_id=id).delete()
            return APIResponse()

        return APIResponse(data_msg=False, status="5001")


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
                    return APIResponse(results=create_token(userName=user.user_name))
        return APIResponse(data_msg=False, status=status.HTTP_401_UNAUTHORIZED)
