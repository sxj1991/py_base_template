from django.db import models


# Create your models here.

class UserModel(models.Model):
    userId = models.AutoField(primary_key=True, db_column="user_id")
    user_name = models.CharField(db_column="user_name", max_length=30)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_user"
