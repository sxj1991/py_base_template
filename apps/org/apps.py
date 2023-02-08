from django.apps import AppConfig


class OrgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.org'


class OrgService(object):
    @staticmethod
    def findUserMatchOrg(user):
        orgs = []
        for o in user.org_model.all():
            org = {
                "orgName": o.org_name
            }
            orgs.append(org)
        return orgs

    @staticmethod
    def findOrgMatchUser(org):
        users = []
        for u in org.user_model.all():
            user = {
                "name": u.user_name,
                "password": u.password
            }
            users.append(user)
        return users
