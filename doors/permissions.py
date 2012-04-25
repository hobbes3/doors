from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from doors.models import Order, Place
from doors.forms import OrderCreateForm, CommentCreateForm

# Returns a list of orders that the user is allowed to view.
def get_viewable_order_list(user):
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
    # Property managers can only see orders if they are the manager of the order's creator's place.
    elif user.profile.has_user_types(['pm']):
        return Order.objects.filter(place__managers=user)
    # Tenants can only see orders that they created.
    elif user.profile.has_user_types(['te']):
        return Order.objects.filter(creator=user)
    else:
        return None

def get_orders_create_dictionary(user, POST_data=None):
    # Only tenants (with a place), property managers, moderators, and administrators can create orders.
    # All moderators and administrators can create orders and assign any creators who are either tenants or project managers.
    if user.profile.has_user_types(['mo', 'ad']):
        creator_list = User.objects.filter(
            Q(userprofile__user_types__name='te') |
            Q(userprofile__user_types__name='pm')
        ).distinct()
        can_assign_creator = 1
    # All property managers can create orders but only assign creators whose property the property manager manages.
    elif user.profile.has_user_types(['pm']):
        creator_list = User.objects.filter(
            Q(userprofile__place__managers=user) |
            Q(pk=user.pk)
        )
        can_assign_creator = 1
    # Next allow tenants to create orders (and not assign creators).
    elif user.profile.has_user_types(['te']):
        # Tenants without a place can't create orders
        if not user.profile.place:
            messages.error(request, "As a tenant, you don't have a property assigned to create an order!")
            return None

        creator_list = User.objects.filter(pk=user.pk)
        can_assign_creator = 0
    # Everyone else left can't create orders.
    else:
        messages.error(request, "Only tenants, property managers, moderators, and administrators can create orders!")
        return None

    form = OrderCreateForm(data=POST_data, creator_list=creator_list)

    if 'creator' in form.data:
        creator = User.objects.get(pk=int(form.data['creator']))

        if creator.profile.has_user_types(['pm']):
            place_list = creator.place_managers.all()
        else:
            place_list = Place.objects.filter(userprofile_place=creator)

        form = OrderCreateForm(data=POST_data, creator_list=creator_list, place_list=place_list)

    return {
        'form': form,
        'can_assign_creator': can_assign_creator
    }

def get_orders_detail_dictionary(order, user, POST_data=None):
    comment_list = order.comment_order.all()
    comment_form = CommentCreateForm(data=POST_data)

    # All property managers, moderators, and administrators can edit orders.
    if user.profile.has_user_types(['pm', 'mo', 'ad']):
        can_edit = 1
    # Everyone else left can't edit orders.
    else:
        can_edit = 0

    return {
        'order': order,
        'comment_list': comment_list,
        'comment_form': comment_form,
        'can_edit': can_edit,
    }
