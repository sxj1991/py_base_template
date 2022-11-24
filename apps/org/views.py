from django.http import StreamingHttpResponse
from rest_framework.views import APIView

from apps.base_response.api_response import APIResponse
from apps.org.models import OrgModel, OrgTypeModel
from apps.org.serializers import OrgTypeSerializer
from py_base_template.decorator import log_resp
import logging

# Create your views here.
logger = logging.getLogger('full_logger')


class OrgViews(APIView):
    def get(self, request, id):
        logger.info(msg=f"接收前端查询数据:request:{request.data}-id:{id}")
        orgType = OrgTypeModel.objects.get(org_type_id=id)
        if orgType:
            serializer = OrgTypeSerializer(instance=orgType)
            return APIResponse(results=serializer.data)
        return APIResponse()


class FileViews(APIView):
    def post(self, request):
        handle_uploaded_file(request.FILES['file'])
        return APIResponse()

    def get(self, request):
        response = StreamingHttpResponse(file_iterator("./file/image.jpg"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=image.jpg'
        return response


def handle_uploaded_file(f):
    with open('./file/image.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            destination.flush()


def file_iterator(file_name, chunk_size=1024):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
