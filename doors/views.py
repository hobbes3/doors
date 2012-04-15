from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from doors.models import Order, User
from doors.forms import OrderCreateForm
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)

# UserType
# TYPE_CHOICES=(
#     ('ad', 'administrator'   ),
#     ('mo', 'moderator'       ),
#     ('vi', 'viewer'          ),
#     ('pm', 'property manager'),
#     ('po', 'property owner'  ),
#     ('vm', 'vendor manager'  ),
#     ('ve', 'vendor'          ),
#     ('te', 'tenant'          ),
#)

class OrderListView(ListView):
    template_name = 'doors/orders/list.html'
    #paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated():
            return None

        # Administrators, moderators, and viewers can see all orders.
        if user.profile.has_user_types(['ad', 'mo', 'vi']):
            return Order.objects.all()
        # Vendors and vendor managers can only see orders that are assigned to them.
        elif user.profile.has_user_types(['ve', 'vm']):
            return Order.objects.filter(
                Q(vendor__managers=user) |
                Q(vendor__representatives=user)
           )
        # Property owners can only see orders if they own the place of the order's creator's place.
        elif user.profile.has_user_types(['po']):
            return Order.objects.filter(place__owners=user)
        # Property managers can only see orders if they are the order's approver.
        elif user.profile.has_user_types(['pm']):
            return Order.objects.filter(approver=user)
        # Tenants can only see orders that they created.
        elif user.profile.has_user_types(['te']):
            return Order.objects.filter(creator=user)
        else:
            return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['all_orders_count'] = Order.objects.count()
        return context

class OrderDetailView(DetailView):
    model = Order
    template_name = 'doors/orders/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(OrderDetailView, self).get_context_data(**kwargs)

        user = self.request.user

        # All property managers, moderators, and administrators can edit orders.
        if user.profile.has_user_types(['pm', 'mo', 'ad']):
            context['can_edit'] = 1
        # Everyone else left can't edit orders.
        else:
            context['can_edit'] = 0

        return context

class SelfUserDetailView(DetailView):
    model = User
    template_name = 'doors/users/detail.html'
    context_object_name = 'user_object'

    def get_object(self):
        return self.request.user

@login_required
def orders_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            creator  = form.cleaned_data['creator' ]
            approver = form.cleaned_data['approver']
            comment  = form.cleaned_data['comment' ]

            new_order = Order.objects.create(
                creator =creator,
                approver=approver,
                comment =comment
            )

            messages.success(request, "Your order #{} had been created!".format(new_order.pk))
            logger.info("{user} created order #{pk}".format(user=request.user, pk=new_order.pk))

            return HttpResponseRedirect(reverse('orders_detail', kwargs={'pk': new_order.pk}))
        else:
            dictionary = {'form', form}
            return render(request, 'doors/orders/create.html', dictionary)

    user = request.user

    # Only tenants (with a place), property managers, moderators, and administrators can create orders.
    # All moderators and administrators can create orders and assign any creators.
    if user.profile.has_user_types(['mo', 'ad']):
        dictionary={
            'creator_list': User.objects.all(),
            'form': OrderCreateForm(),
            'can_assign_creator': 1,
        }

        return render(request, 'doors/orders/create.html', dictionary)
    # All property managers can create orders but only assign creators whose property the property manager manages.
    elif user.profile.has_user_types(['pm']):
        creator_list = User.objects.filter(
            Q(userprofile__place__managers=user) |
            Q(pk=user.pk)
        )

        dictionary={
            'creator_list': creator_list,
            'form': OrderCreateForm(),
            'can_assign_creator': 1,
        }

        return render(request, 'doors/orders/create.html', dictionary)
    # Next allow tenants to create orders (and not assign creators).
    elif user.profile.has_user_types(['te']):
        # Tenants without a place can't create orders
        if not user.profile.place:
            messages.error(request, "As a tenant, you don't have a property assigned to create an order!")

            return HttpResponseRedirect(reverse('orders_list'))

        dictionary={
            'form': OrderCreateForm(),
            'can_assign_creator': 0,
        }

        return render(request, 'doors/orders/create.html', dictionary)
    # Everyone else left can't create orders.
    else:
        messages.error(request, "Only tenants, property managers, moderators, and administrators can create orders!")

        return HttpResponseRedirect(reverse('orders_list'))
