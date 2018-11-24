from leagueOfDrivers.settings import AUTH_USER_MODEL as USER
from django.core.exceptions import ObjectDoesNotExist
from wx_league import models as wx_league
from share import models as share


def check_cookie(self, user_type):
    try:
        cookie = self.request.query_params.get("cookie", None)
        user = eval(USER).objects.get(cookie=cookie)
    except ObjectDoesNotExist:
        return False
    userobj = {
        "Uesr": user,
        "ShareUser": share.ShareUser.objects.get(user=user),
        "ShareUserProfile": share.ShareUserProfile.objects.get(user=share.ShareUser.objects.get(user=user))
    }.get(user_type, False)

    return {"userobj": userobj, "user": user}
