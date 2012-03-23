from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, DetailView
from doors.models import Order

urlpatterns = patterns( 'doors.views',
    url( r'^orders/$'                               , 'orders_list'        , name = 'orders_list'         ),
    url( r'^orders/(?P<order_id>\d+)/$'             , 'orders_detail'      , name = 'orders_detail'       ),
    url( r'^orders/(?P<order_id>\d+)/comments/add/$', 'orders_comments_add', name = 'orders_comments_add' ),
    url( r'^orders/create/$'                        , 'orders_create'      , name = 'orders_create'       ),
)
