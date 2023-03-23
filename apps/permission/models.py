from enum import Enum, unique

from django.db import models


# 角色模型
class RoleModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    role_name = models.CharField(db_column="role_name", max_length=30)

    class Meta:
        db_table = "tb_role"


# 用户角色模型
class UserRoleModel(models.Model):
    user_id = models.IntegerField(db_column="user_id")
    role_id = models.IntegerField(db_column="role_id")

    class Meta:
        db_table = "tb_user_role"


# 菜单模型
class MenuModel(models.Model):
    menu_name = models.CharField(db_column="menu_name", max_length=30)
    parent_id = models.IntegerField(db_column="parent_id")
    perms = models.CharField(db_column="perms", max_length=30)

    class Meta:
        db_table = "tb_menu"


# 角色菜单模型
class RoleMenuModel(models.Model):
    role_id = models.IntegerField(db_column="role_id")
    menu_id = models.IntegerField(db_column="menu_id")

    class Meta:
        db_table = "tb_role_menu"


class PermissionModel(models.Model):
    name = models.CharField(db_column="name", null=False, max_length=50, help_text="权限名称")
    permission_type = models.CharField(db_column="type", null=False, max_length=20,
                                       help_text="类型", unique=True)
    use_scope = models.CharField(db_column="scope", null=False, max_length=20, help_text="使用范围")

    class Meta:
        db_table = "tb_permission"

    # @unique 装饰器确保枚举类 值唯一不会重复 模型数据库没有关系 模型字段unique属性设置
    # 唯一约束： 数据库该值在表中唯一，不能重复
    # str 不用.value 直接获取值
    @unique
    class PermissionType(str, Enum):
        USER_TYPE = "user_type"
        USE_TYPE = "use_type"

