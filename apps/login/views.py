from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import UserModel
from apps.base_response.api_response import APIResponse
from .utils import create_token


# Create your views here.


class UserView(APIView):

    def get(self, request, id):
        user = UserModel.objects.filter(userId=id).first()

        if user:
            serializer = UserSerializer(instance=user)
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
                else:
                    return APIResponse(data_msg=False, results=serializer.errors, status="5001")
        return APIResponse()


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