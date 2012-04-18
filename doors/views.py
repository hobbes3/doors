from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from doors.models import Order, User, Place
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
    def get_order_create_dictionary(user):
        # Only tenants (with a place), property managers, moderators, and administrators can create orders.
        # All moderators and administrators can create orders and assign any creators who are either tenants or project managers.
        if user.profile.has_user_types(['mo', 'ad']):
            creator_list = User.objects.filter(
                Q(userprofile__user_types__name='te') |
                Q(userprofile__user_types__name='pm')
            ).distinct()

            return {
                'creator_list': creator_list,
                'can_assign_creator': 1,
            }
        # All property managers can create orders but only assign creators whose property the property manager manages.
        elif user.profile.has_user_types(['pm']):
            creator_list = User.objects.filter(
                Q(userprofile__place__managers=user) |
                Q(pk=user.pk)
            )

            return {
                'creator_list': creator_list,
                'can_assign_creator': 1,
            }
        # Next allow tenants to create orders (and not assign creators).
        elif user.profile.has_user_types(['te']):
            # Tenants without a place can't create orders
            if not user.profile.place:
                messages.error(request, "As a tenant, you don't have a property assigned to create an order!")
                return False

            return {
                'creator_list': None,
                'can_assign_creator': 0,
            }
        # Everyone else left can't create orders.
        else:
            messages.error(request, "Only tenants, property managers, moderators, and administrators can create orders!")
            return False

    user = request.user
    dictionary = get_order_create_dictionary(user)

    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()

        form = OrderCreateForm(data=request.POST, creator_list=dictionary['creator_list'])

        creator_pk = form.data['creator']

        if creator_pk:
            creator = User.objects.get(pk=int(creator_pk))

            if creator.profile.has_user_types(['pm']):
                place_list = creator.place_managers.all()
            else:
                place_list = Place.objects.filter(userprofile_place=creator)
                #place_list = creator.profile.place # This won't work since it returns a single object, not a QuerySet.

            form = OrderCreateForm(data=request.POST, creator_list=dictionary['creator_list'], place_list=place_list)

        if form.is_valid():
            creator   = form.cleaned_data['creator']
            place     = form.cleaned_data['place']
            work_type = form.cleaned_data['work_type']
            comment   = form.cleaned_data['comment']

            new_order = Order.objects.create(
                creator  =creator,
                place    =place,
                work_type=work_type,
                comment  =comment
            )

            messages.success(request, "Your order #{} had been created!".format(new_order.pk))
            logger.info("{user} created order #{pk}".format(user=user, pk=new_order.pk))

            return HttpResponseRedirect(reverse('orders_detail', kwargs={'pk': new_order.pk}))
        else:
            return render(request, 'doors/orders/create.html', {'form': form, 'can_assign_creator': dictionary['can_assign_creator']})
    # Not POST.
    else:
        if dictionary:
            return render(request, 'doors/orders/create.html', {
                'form': OrderCreateForm(creator_list=dictionary['creator_list']),
                'can_assign_creator': dictionary['can_assign_creator']
            })
        else:
            # Messages called in get_order_create_dictionary().
            return HttpResponseRedirect(reverse('orders_list'))
