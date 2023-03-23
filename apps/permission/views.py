from rest_framework.views import APIView

from apps.base_response.api_response import APIResponse
from apps.permission.models import PermissionModel


# 用户权限设计
class PermissionViews(APIView):
    def get(self, request):
        name = request.GET.get("name", "默认权限")
        scope = request.GET.get("scope", "默认范围")
        permission_type = request.GET.get("permission_type", "默认类型")
        PermissionModel.objects.create(name=name, permission_type=PermissionModel.PermissionType.USE_TYPE,
                                       use_scope=scope)
        try:
            permission_enum = PermissionModel.PermissionType(permission_type)
            msg(permission_enum)
        except ValueError as e:
            print(e.__str__())
            return APIResponse(data_msg='权限类型超出范围,请重新填写')

        return APIResponse()


def msg(permission_type: PermissionModel.PermissionType):
    print(f'权限类型:{permission_type.value}-{permission_type.name}')
