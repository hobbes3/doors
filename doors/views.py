from django.shortcuts import render, get_object_or_404
from doors.models import *
from doors.forms import AddComment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def orders_detail( request, pk ) :
    order          = get_object_or_404( Order, pk = pk )
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

def users_detail( request, pk ) :
    user = get_object_or_404( User, pk = pk )

    return HttpResponse( "users_detail for {username}".format( username = user.username ) )

@login_required
def users_self_detail( request ) :
    return users_detail( request, request.user.pk )
