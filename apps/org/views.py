from django.http import StreamingHttpResponse
from rest_framework.views import APIView

from apps.base_response.api_response import APIResponse
from apps.org.models import OrgModel, OrgTypeModel
from apps.org.serializers import OrgTypeSerializer
from apps.org.threadPool import start_thread
from py_base_template.decorator import log_resp
import logging

# Create your views here.
logger = logging.getLogger('full_logger')


class OrgViews(APIView):
    def get(self, request, id):
        role = request.data.get("role")
        logger.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}-role:{role}")
        orgType = OrgTypeModel.objects.get(org_type_id=id)
        role_dict = {
            "default": self.__print_msg_default,
            "admin": self.__print_msg_admin
        }
        data = {
            "role": role
        }
        # 字典根据role传入值选择其中的函数引用,根据data解构的参数执行方法
        role_dict[role](**data)
        if orgType:
            serializer = OrgTypeSerializer(instance=orgType)
            return APIResponse(results=serializer.data)
        return APIResponse()

    @classmethod
    def __print_msg_default(cls, role):
        print(f"msg_default:{role}")

    @classmethod
    def __print_msg_admin(cls, role):
        print(f"msg_admin:{role}")

    def post(self, request, id):
        logger.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}")
        org = OrgTypeModel()
        org.org_type = "newType"
        org.save()
        return APIResponse()


class FileViews(APIView):
    def post(self, request):
        if request.FILES.get('image'):
            # 上传图片文件
            handle_uploaded_file(request.FILES['image'])
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
