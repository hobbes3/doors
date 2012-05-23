from django.conf import settings
from django.contrib.sites.models import Site

def current_site(request):
    try:
        current_site = Site.objects.get_current()
        return {
            'site': current_site,
        }
    except Site.DoesNotExist:
        return {
            'site': '',
        }

def booleans():
    return {
        'True': True,
        'False': False,
    }

def is_certain_user_type(request):
    if request.user.is_anonymous():
        return {}

    return {
        'is_administrator':    request.user.profile.has_user_types(['ad']),
        'is_moderator':        request.user.profile.has_user_types(['mo']),
        'is_viewer':           request.user.profile.has_user_types(['vi']),
        'is_property_manager': request.user.profile.has_user_types(['pm']),
        'is_property_owner':   request.user.profile.has_user_types(['po']),
        'is_vendor_manager':   request.user.profile.has_user_types(['vm']),
        'is_vendor':           request.user.profile.has_user_types(['ve']),
        'is_tenant':           request.user.profile.has_user_types(['te']),
    }
