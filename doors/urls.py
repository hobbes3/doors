from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns( 'doors.views',
    url( r'^$'                             , 'index'          ),
    url( r'^order/(?P<order_id>\d+)/$'     , 'order_detail'   ),
    url( r'^order/user/(?P<username>\w+)/$', 'order_username' ),
    url( r'^order/all/'                    , 'order_all'      ),
)
