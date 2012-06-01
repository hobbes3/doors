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
