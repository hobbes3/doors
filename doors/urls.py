from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from doors.models import Order, Vendor, Place
from doors.views import *

# The order should be
# List
# Create (Create)
# Detail (Read)
# Edit   (Update)
# Delete (Delete)
# Special

urlpatterns = patterns('doors.views',
    # Order
    url(r'^orders/$', OrderListView.as_view(), name='orders_list'),
    url(r'^orders/create/$', 'orders_create', name='orders_create'),
    url(r'^orders/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='orders_detail'),
    # User
    url(
        r'^users/$',
        ListView.as_view(
            model=User,
            template_name='doors/users/list.html',
        ),
        name='users_list'
    ),
    url(
        r'^users/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=User,
            template_name='doors/users/detail.html',
            context_object_name='user_object'
        ),
        name='users_detail'
    ),
    url(r'^users/self/$', login_required(SelfUserDetailView.as_view()), name='users_self_detail'),
    # Vendor
    url(
        r'^vendors/$',
        ListView.as_view(
            model=Vendor,
            template_name='doors/vendors/list.html',
        ),
        name='vendors_list'
    ),
    url(
        r'^vendors/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Vendor,
            template_name='doors/vendors/detail.html',
        ),
        name='vendors_detail'
    ),
    # Place
    url(
        r'^places/$',
        ListView.as_view(
            model=Place,
            template_name='doors/places/list.html',
        ),
        name='places_list'
    ),
    url(
        r'^places/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Place,
            template_name='doors/places/detail.html',
        ),
        name='places_detail'
    ),
)
