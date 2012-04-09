from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from doors.models import *
from doors.forms import OrderCreateForm
import logging

logger = logging.getLogger(__name__)

# UserType
# TYPE_CHOICES = (
#     ( 'ad', 'administrator'    ),
#     ( 'mo', 'moderator'        ),
#     ( 'vi', 'viewer'           ),
#     ( 'pm', 'property manager' ),
#     ( 'po', 'property owner'   ),
#     ( 'vm', 'vendor manager'   ),
#     ( 've', 'vendor'           ),
#     ( 'te', 'tenant'           ),
# )

class OrderListView( ListView ) :
    template_name = 'doors/orders/list.html'
    #paginate_by = 10

    def get_queryset( self ) :
        user = self.request.user

        if not user.is_authenticated() :
            return None

        # Administrators, moderators, and viewers can see all orders.
        if user.profile.has_user_types( [ 'ad', 'mo', 'vi' ] ) :
            return Order.objects.all()
        # Vendors and vendor managers can only see orders that are assigned to them.
        elif user.profile.has_user_types( [ 've', 'vm' ] ) :
            return Order.objects.filter(
                Q( vendor__managers = user.pk ) |
                Q( vendor__representatives = user.pk )
            )
        # Property owners can only see orders if they own the place of the order's creator's place.
        elif user.profile.has_user_types( [ 'po' ] ) :
            return Order.objects.filter( place__owners = user.pk )
        # Property managers can only see orders if they are the order's approver.
        elif user.profile.has_user_types( [ 'pm' ] ) :
            return Order.objects.filter( approver = user.pk )
        # Tenants can only see orders that they created.
        elif user.profile.has_user_types( [ 'te' ] ) :
            return Order.objects.filter( creator = user.pk )
        else :
            return None

    def get_context_data( self, **kwargs ) :
        # Call the base implementation first to get a context.
        context = super( OrderListView, self ).get_context_data( **kwargs )
        context[ 'all_orders_count' ] = Order.objects.count()
        return context

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

            messages.add_message( request, messages.SUCCESS, "Your order #{pk} had been created!".format( pk = new_order.pk ) )
            logger.info( "{user} created order #{pk}".format( user = request.user, pk = new_order.pk ) )

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
