from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from doors.models import Order, Vendor, Property
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
    url(r'^order/$', OrderListView.as_view(), name='order_list'),
    url(r'^order/create/$', 'order_create', name='order_create'),
    url(r'^order/(?P<pk>\d+)/$', 'order_detail', name='order_detail'),
    url(r'^order/(?P<pk>\d+)/edit/$', 'order_edit', name='order_edit'),
    # Comment
    url(r'^order/(?P<order_pk>\d+)/comment/create/$', 'comment_create', name='comment_create'),
    # User
    url(r'^user/$', UserListView.as_view(), name='user_list'),
    url(r'^user/(?P<pk>\d+)/$', 'user_detail', name='user_detail'),
    url(r'^user/self/$', 'user_self_detail', name='user_self_detail'),
    # Vendor
    url(r'^vendor/$', VendorListView.as_view(), name='vendor_list'),
    url(
        r'^vendor/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Vendor,
            template_name='doors/vendor/detail.html',
        ),
        name='vendor_detail'
    ),
    # Property
    url(r'^property/$', PropertyListView.as_view(), name='property_list'),
    url(
        r'^property/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Property,
            template_name='doors/property/detail.html',
        ),
        name='property_detail'
    ),
)
