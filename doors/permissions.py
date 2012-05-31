from django import forms
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from doors.models import Order, Place
from doors.forms import CustomDateTimeField, OrderCreateForm, CommentCreateForm
from itertools import chain

# Returns a list of orders that the user is allowed to view.
def get_viewable_order_list(user):
    if not user.is_authenticated():
        return Order.objects.none()

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

def get_order_create_dictionary(user, POST_data=None):
    # Only tenants (with a place), property managers, moderators, and administrators can create orders.
    # All moderators and administrators can create orders and assign any creators who are either tenants or project managers.
    if user.profile.has_user_types(['mo', 'ad']):
        creator_list = User.objects.filter(
            Q(userprofile_from_user__user_types__name='te') |
            Q(userprofile_from_user__user_types__name='pm')
        ).distinct()
        can_edit_creator = 1
    # All property managers can create orders but only assign creators whose property the property manager manages.
    elif user.profile.has_user_types(['pm']):
        creator_list = User.objects.filter(
            Q(userprofile_from_user__place__managers=user) |
            Q(pk=user.pk)
        )
        can_edit_creator = 1
    # Next allow tenants to create orders (and not assign creators).
    elif user.profile.has_user_types(['te']):
        # Tenants without a place can't create orders
        if not user.profile.place:
            messages.error(request, "As a tenant, you don't have a property assigned to create an order!")
            return None

        creator_list = User.objects.filter(pk=user.pk)
        can_edit_creator = 0
    # Everyone else left can't create orders.
    else:
        messages.error(request, "Only tenants, property managers, moderators, and administrators can create orders!")
        return None

    form = OrderCreateForm(data=POST_data, creator_list=creator_list)

    if 'creator' in form.data and form.data['creator']:
        creator = User.objects.get(pk=int(form.data['creator']))

        if creator.profile.has_user_types(['pm']):
            place_list = creator.places_from_managers.all()
        else:
            # place_list needs to be a QuerySet. Therefore you can't just do "creator.profile.place".
            place_list = Place.objects.filter(userprofiles_from_place__user=creator)

        form = OrderCreateForm(data=POST_data, creator_list=creator_list, place_list=place_list)

    return {
        'form': form,
        'can_edit_creator': can_edit_creator
    }

def get_order_detail_dictionary(order, user, POST_data=None):
    can_delete       = 0
    can_assign       = 0
    can_check_steps  = 0
    can_comment      = 0

    custom_widgets = {
        'status':                forms.RadioSelect(),
        'fa_status_creator':     forms.RadioSelect(),
        'fa_status_vendor':      forms.RadioSelect(),
        'quote_status_approver': forms.RadioSelect(),
        'quote_status_owner':    forms.RadioSelect(),
        'sa_status_creator':     forms.RadioSelect(),
        'sa_status_vendor':      forms.RadioSelect(),
    }

    if user.profile.has_user_types(['mo', 'ad']):
        can_delete      = 1
        can_assign      = 1
        can_check_steps = 1
        can_comment     = 1

        include_fields = (
            'status',
            'work_type',
            'note',
            'vendor',
            'fa_date',
            'fa_duration',
            'fa_status_creator',
            'fa_status_vendor',
            'quote',
            'quote_status_approver',
            'quote_status_owner',
            'sa_date',
            'sa_duration',
            'sa_status_creator',
            'sa_status_vendor',
            'payment',
        )
    elif user.profile.has_user_types(['pm']):
        can_delete      = 1
        can_assign      = 1
        can_check_steps = 1
        can_comment     = 1

        include_fields = (
            'status',
            'work_type',
            'note',
            'vendor',
            'quote_status_approver',
        )
    elif user.profile.has_user_types(['po']):
        can_comment     = 1

        include_fields = (
            'quote_status_owner',
        )
    elif user.profile.has_user_types(['vm', 've']):
        can_comment     = 1

        include_fields = (
            'fa_date',
            'fa_duration',
            'fa_status_vendor',
            'quote',
            'sa_date',
            'sa_duration',
            'sa_status_vendor',
            'payment',
        )
    elif user.profile.has_user_types(['te']):
        can_comment     = 1

        include_fields = (
            'fa_date',
            'fa_status_creator',
            'sa_date',
            'sa_status_creator',
        )
    else:
        return {
            'order': order,
            'order_form': None,
            'comment_form': None,
            'can_delete': can_delete,
            'can_assign': can_assign,
            'can_check_steps': can_check_steps,
            'can_comment': can_comment,
        }

    class OrderDetailForm(forms.ModelForm):
        if 'fa_date' in include_fields:
            fa_date = CustomDateTimeField(label="first appointment time")
        if 'sa_date' in include_fields:
            sa_date = CustomDateTimeField(label="second appointment time")

        class Meta:
            model = Order
            fields = include_fields
            widgets = custom_widgets

        def clean(self):
            super(OrderDetailForm, self).clean()

            if 'note' in self.cleaned_data:
                if len(self.cleaned_data['note']) < 50:
                    self._errors['note'] = self.error_class([u"Please enter a longer note."])

                    del self.cleaned_data['note']

            return self.cleaned_data

    order_form = OrderDetailForm(data=POST_data, instance=order)

    comment_form = CommentCreateForm(data=POST_data)

    return {
        'order': order,
        'order_form': order_form,
        'comment_form': comment_form,
        'can_delete': can_delete,
        'can_assign': can_assign,
        'can_check_steps': can_check_steps,
        'can_comment': can_comment,
    }
