from django.db import models

from apps.login.models import UserModel


# 组织模型类


class OrgModel(models.Model):
    org_id = models.AutoField(primary_key=True, db_column="org_id")
    org_name = models.CharField(max_length=50)
    user_model = models.ManyToManyField(UserModel, through="UserOrgModel", through_fields=('orgs_id', 'users_id'))
    org_type_id = models.ForeignKey('OrgTypeModel', on_delete=models.CASCADE, db_column="org_type_id")

    class Meta:
        default_related_name = "org_model"
        db_table = "tb_org"

    def __str__(self):
        return self.org_id


class UserOrgModel(models.Model):
    users_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_column="user_id")
    orgs_id = models.ForeignKey(OrgModel, on_delete=models.CASCADE, db_column="org_id")

    class Meta:
        db_table = "tb_org_user"

    def __str__(self):
        return self


# 组织类型模型类
class OrgTypeModel(models.Model):
    org_type_id = models.AutoField(primary_key=True, db_column="org_type_id")
    org_type = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_org_type"

    def __str__(self):
        return self.org_type_id
