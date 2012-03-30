from django.shortcuts import render, get_object_or_404
from doors.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

class SelfUserDetailView( DetailView ) :
    model               = User
    template_name       = 'doors/users/detail.html'
    context_object_name = 'user_object'

    def get_object( self ) :
        return self.request.user

@login_required
def orders_create( request ) :
    if request.method == 'POST' :
        form = OrderCreateForm( request.POST )
        if form.is_valid() :
            creator  = form.cleaned_data[ 'creator'  ]
            approver = form.cleaned_data[ 'approver' ]
            comment  = form.cleaned_data[ 'comment'  ]

            new_order = Order.objects.create(
                creator  = creator,
                approver = approver,
                comment  = comment
            )

            messages.add_message( request, messages.SUCCESS, "Your order number #{pk} had been created!".format( pk = new_order.pk ) )

            return HttpResponseRedirect( reverse( 'orders_detail', kwargs = { 'pk' : new_order.pk } ) )
    else :
        form = OrderCreateForm()

    if request.user.profile.user_types.filter( pk = 2 ) : # property manager
        manager = 1
    else :
        manager = 0

    try :
        approver = request.user.profile.place.manager
    except AttributeError :
        approver = 0

    dictionary = {
        'form'     : form,
        'approver' : approver,
        'manager'  : manager,
    }

    return render( request, 'doors/orders/create.html', dictionary )
