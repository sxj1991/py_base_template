import json

from django.core import serializers
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage

from apps.base_response.api_response import APIResponse
from apps.login.models import UserModel
from apps.org.apps import OrgService
from apps.org.models import OrgModel, OrgTypeModel
from apps.org.serializers import OrgTypeSerializer
from apps.org.threadPool import start_thread
import logging

# Create your views here.
logger = logging.getLogger('full_logger')

org_service = OrgService()


class OrgViews(APIView):
    def get(self, request, id):
        # 获取前端参数方式 request.GET.get
        role = request.GET.get("role")

        logger.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}-role:{role}-")
        org_type = OrgTypeModel.objects.get(org_type_id=id)
        self.strategy_dict(role)
        if org_type:
            serializer = OrgTypeSerializer(instance=org_type)
            return APIResponse(results=serializer.data)
        return APIResponse()

    def strategy_dict(self, role):
        data = {
            "role": role
        }
        role_dict = {
            "default": self.__print_msg_default,
            "admin": self.__print_msg_admin
        }
        # 字典根据role传入值选择其中的函数引用,根据data解构的参数执行方法
        role_dict[role](**data)

    @classmethod
    def __print_msg_default(cls, role):
        print(f"msg_default:{role}")

    @classmethod
    def __print_msg_admin(cls, role):
        print(f"msg_admin:{role}")

    def put(self, request, id):
        # 获取前端参数方式 request.data.get
        # role = request.data.get("role")
        # 获取前端参数方式 json
        json_body = json.loads(request.body)
        role_json = json_body.get("role")

        logger.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}-role_json:{role_json}")
        org = OrgTypeModel()
        org.org_type = "newType"
        org.save()
        return APIResponse()

    def post(self, request, id):
        logger.info(msg=f"接收前端查询数据id:{id}")
        match = request.data["match"]

        if match == "org":
            org = OrgModel.objects.filter(pk=id).first()
            data = org_service.find_org_match_user(org)

        else:
            user = UserModel.objects.filter(pk=id).first()
            data = org_service.find_user_match_org(user)

        return APIResponse(results=data)


class FileViews(APIView):
    def post(self, request):
        if request.FILES.get('image'):
            # 原生上传图片文件
            handle_uploaded_file(request.FILES['image'])
            # django fileSystemStorage 上传
            fs = FileSystemStorage()
            fs.save("fileSystemStorage_save.jpg", request.FILES['image'])
            upload_path = fs.path("fileSystemStorage_save.jpg")
            logger.info(msg=f"上传路径:{upload_path}")
        elif request.FILES.get('file'):
            # 读取文件内容
            attr_value = request.FILES['file'].read()
            if type(attr_value) is bytes:
                start_thread(str(attr_value, encoding='utf-8'))
                logger.info(f"读取文件内容:{str(attr_value, encoding='utf-8')}")
            elif type(attr_value) is str:
                start_thread(str(attr_value, encoding='utf-8'))
                logger.info(f"读取文件内容:{attr_value}")
        return APIResponse()

    def get(self, request):
        # 下载文件
        response = StreamingHttpResponse(file_iterator("./file/image.jpg"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=image.jpg'
        return response


def handle_uploaded_file(f):
    with open('./file/image.jpg', 'wb+') as destination:
        for chunk in f.nks():
            destination.wchurite(chunk)
            destination.flush()


def file_iterator(file_name, chunk_size=1024):
    with open(file_name, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break
