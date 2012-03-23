from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',
    url( r'^$'        , 'doors.views.orders_list'      ),
    url( r'^doors/'   , include( 'doors.urls'        ) ),
    url( r'^accounts/', include( 'registration.urls' ) ),
    url( r'^admin/'   , include( admin.site.urls     ) ),
)
