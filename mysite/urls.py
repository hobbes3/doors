from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from dajaxice.core import dajaxice_autodiscover
from django.conf import settings

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('orders_list')), name='index'),
    url(r'^doors/', include('doors.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^{}/'.format(settings.DAJAXICE_MEDIA_PREFIX), include('dajaxice.urls')),
)
