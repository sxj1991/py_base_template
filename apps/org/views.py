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
