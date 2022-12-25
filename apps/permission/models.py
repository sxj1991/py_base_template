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
