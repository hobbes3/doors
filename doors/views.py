from django.shortcuts import render, get_object_or_404
from doors.models import *
from doors.forms import AddComment

def orders_list( request ) :
    orders = Order.objects.all()

    dictionary = {
        'orders' : orders,
    }

    return render( request, 'doors/orders/list.html', dictionary )

def orders_detail( request, order_id ) :
    order          = get_object_or_404( Order, pk = order_id )
    order_comments = order.ordercomment_set.all()

    if request.method == 'POST' :
        comment_form = AddComment( request.POST )

        if comment_form.is_valid() :
            cd = comment_form.cleaned_data

            OrderComment.objects.create(
                order   = order,
                author  = request.user,
                comment = cd[ 'comment' ],
            )
    else :
        comment_form = AddComment()

    dictionary = {
        'order'          : order,
        'order_comments' : order_comments,
        'comment_form'   : comment_form,
    }

    return render( request, 'doors/orders/detail.html', dictionary )

def orders_create( request ) :
    pass

def orders_comments_add( request ) :
    pass
