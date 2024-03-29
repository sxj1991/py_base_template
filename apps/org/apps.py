from django.apps import AppConfig


class OrgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.org'


class OrgService(object):
    @staticmethod
    def find_user_match_org(user):
        args = []
        # org_model 反向查询 用户对应的组织信息
        for o in user.org_model.all():
            org = {
                "orgName": o.org_name
            }
            args.append(org)

        data = {
            "org": args,
            "user": user.user_name
        }
        return data

    @staticmethod
    def find_org_match_user(org):
        users = []
        # 查询组织对应的用户信息
        for u in org.user_model.all():
            user = {
                "name": u.user_name,
                "password": u.password
            }
            users.append(user)
        data = {
            "users": users,
            "org": org.org_name
        }
        return data
