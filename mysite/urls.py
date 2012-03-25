from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns( '',
    url( r'^$'        , RedirectView.as_view( url = reverse_lazy( 'orders_list' ) ) ),
    url( r'^doors/'   , include( 'doors.urls'        ) ),
    url( r'^accounts/', include( 'registration.urls' ) ),
    url( r'^admin/'   , include( admin.site.urls     ) ),
)
