from django.shortcuts import render_to_response, get_object_or_404
from doors.models import *

def index( request ) :
    pass

def order_detail( request, order_id ) :
    order    = get_object_or_404( Order, pk = order_id )
    comments = OrderComment.objects.filter( order = order_id )

    dictionary = {
        'order'    : order,
        'comments' : comments,
    }

    return render_to_response( 'doors/order/detail.html', dictionary )

def order_username( request, username ) :
    pass

def order_all( request ) :
    orders = Order.objects.all()
    return render_to_response( 'doors/order/list.html', { 'orders' : orders } )
