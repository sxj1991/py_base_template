from rest_framework import serializers

from apps.login.models import UserModel, DetailModel
from apps.permission.models import UserRoleModel, RoleModel, RoleMenuModel, MenuModel


# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="user_id", required=False)
    userName = serializers.CharField(max_length=30, source="user_name")
    detail = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()
    createTime = serializers.DateTimeField(source="create_time", required=False, format="%Y-%m-%d %H:%M:%S")


    def get_detail(self, obj):
        user = obj
        details = DetailModel.objects.filter(user_id=user.user_id)

        ret = []
        for item in details:
            ret.append({"address": item.address, "email": item.email})
        return ret

    def get_role(self, obj):
        user = obj
        userRoles = UserRoleModel.objects.filter(user_id=user.user_id)
        ret = []
        for userRole in userRoles:
            role = RoleModel.objects.filter(id=userRole.role_id).first()
            ret.append({"roleName": role.role_name})
        return ret

    def get_menu(self, obj):
        user = obj
        userRoles = UserRoleModel.objects.filter(user_id=user.user_id)
        ret = []
        for userRole in userRoles:
            roleMenus = RoleMenuModel.objects.filter(role_id=userRole.role_id)
            for roleMenu in roleMenus:
                menu = MenuModel.objects.filter(id=roleMenu.menu_id).first()
                ret.append({"menuName": menu.menu_name, "permission": menu.perms})
        return ret

    def validate(self, attrs):
        name = attrs.get('user_name')
        # 验证参数
        if name == "xxx":
            raise RuntimeError("名字不允许")
        return attrs

    class Meta:
        model = UserModel
        exclude = ['user_name', 'user_id', 'create_time', 'password']
