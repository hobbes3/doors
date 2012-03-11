from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from doors.models import *

def index( request ) :
    pass

def order_detail( request, order_id ) :
    order    = get_object_or_404( Order, pk = order_id )
    comments = OrderComment.objects.filter( order = order_id )

    request_context = RequestContext( request, {
        'order'    : order,
        'comments' : comments,
    } )

    return render_to_response( 'doors/order/detail.html', context_instance = request_context )

def order_username( request, username ) :
    pass

def order_all( request ) :
    orders = Order.objects.all()

    request_context = RequestContext( request, {
        'orders' : orders,
    } )

    return render_to_response( 'doors/order/list.html', context_instance = request_context )

def order_create( request ) :
    pass
