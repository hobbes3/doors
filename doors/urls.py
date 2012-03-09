from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns( 'doors.views',
    url( r'^$'                             , 'index'         , name = 'index'          ),
    url( r'^order/(?P<order_id>\d+)/$'     , 'order_detail'  , name = 'order_detail'   ),
    url( r'^order/user/(?P<username>\w+)/$', 'order_username', name = 'order_username' ),
    url( r'^order/all/'                    , 'order_all'     , name = 'order_all'      ),
    url( r'^order/create/'                 , 'order_create'  , name = 'order_create'   ),
)
