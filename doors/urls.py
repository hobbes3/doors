from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, CreateView, DetailView
from doors.models import Order
from django.contrib.auth.models import User

urlpatterns = patterns( 'doors.views',
    url(
        r'^orders/$',
        ListView.as_view(
            model = Order,
            template_name = 'doors/orders/list.html'
        ),
        name = 'orders_list'
    ),
    url(
        r'^orders/create/$',
        CreateView.as_view(
            model = Order,
            template_name = 'doors/orders/create.html'
        ),
        name = 'orders_create'
    ),
    url( r'^orders/(?P<pk>\d+)/$'             , 'orders_detail'      , name = 'orders_detail'       ),
    url( r'^orders/(?P<pk>\d+)/comments/add/$', 'orders_comments_add', name = 'orders_comments_add' ),

    url(
        r'^users/$',
        ListView.as_view(
            model = User,
            template_name = 'doors/users/list.html'
        ),
    ),
    url( r'^users/(?P<pk>\d+)/$', 'users_detail'     , name = 'users_detail'      ),
    url( r'^users/self/$'       , 'users_self_detail', name = 'users_self_detail' ),
)
