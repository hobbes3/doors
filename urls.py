#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',
    url( r'^polls/', include( 'polls.urls' ) ),
    url( r'^todo/' , include( 'todo.urls'  ) ),
    url( r'^doors/', include( 'doors.urls' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
)
