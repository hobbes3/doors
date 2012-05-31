from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from doors.models import Order, Place, Vendor, Comment
from doors.permissions import *
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
    template_name = 'doors/order/list.html'

    def get_queryset(self):
        return get_viewable_order_list(self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['all_order_count'] = Order.objects.count()
        return context

@login_required
def order_detail(request, pk):
    user = request.user
    order = get_object_or_404(Order, pk=pk)

    if order not in get_viewable_order_list(request.user):
        messages.error(request, "You don't have permission to view order #{}!".format(pk))

        return HttpResponseRedirect(reverse('order_list'))

    return render(request, 'doors/order/detail.html', get_order_detail_dictionary(order=order, user=user))

@login_required
def order_create(request):
    user = request.user

    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()
        dictionary = get_order_create_dictionary(user=user, POST_data=request.POST)

        form = dictionary['form']

        if form.is_valid():
            creator   = form.cleaned_data['creator']
            place     = form.cleaned_data['place']
            work_type = form.cleaned_data['work_type']
            note      = form.cleaned_data['note']

            new_order = Order.objects.create(
                creator=creator,
                place=place,
                work_type=work_type,
                note=note
            )

            messages.success(request, "Your order #{} had been created!".format(new_order.pk))
            logger.info("{user} created order #{pk}".format(user=user, pk=new_order.pk))

            return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': new_order.pk}))
    # Not POST.
    else:
        dictionary = get_order_create_dictionary(user=user)
        if dictionary is None:
            # Messages called in get_order_create_dictionary().
            return HttpResponseRedirect(reverse('order_list'))

    return render(request, 'doors/order/create.html', dictionary)

@login_required
def order_edit(request, pk):
    user = request.user
    order = Order.objects.get(pk=pk)
    focus = None

    #import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        dictionary = get_order_detail_dictionary(order=order, user=user, POST_data=request.POST)
        form = dictionary['order_form']

        if form.is_valid():
            form.save()
        else:
            focus = 'id_work_type'

    url = reverse('order_detail', kwargs={'pk': pk})
    if focus:
        url += "?focus=" + focus

    return HttpResponseRedirect(url)

@login_required
def comment_create(request, order_pk):
    user = request.user
    order = Order.objects.get(pk=order_pk)

    #import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        dictionary = get_order_detail_dictionary(order=order, user=user, POST_data=request.POST)
        form = dictionary['comment_form']

        if form.is_valid():
            comment = form.cleaned_data['comment']

            new_comment = Comment.objects.create(
                order=order,
                user=user,
                action_type='comme',
                comment=comment
            )

            messages.success(request, "Your comment had been posted!")
            logger.info("{user} created comment #{pk} for order #{order_pk}".format(user=user, pk=new_comment.pk, order_pk=order_pk))
        else:
            dictionary['focus'] = 'comment_form'
            return render(request, 'doors/order/detail.html', dictionary)

    return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': order_pk}))

class UserListView(ListView):
    model = User
    template_name = 'doors/user/list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['all_user_count'] = User.objects.count()
        return context

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    dictionary = {
        # Have to use "user_object" because "user" is the logged-in user.
        'user_object': user,
    }

    return render(request, 'doors/user/detail.html', dictionary)

@login_required
def user_self_detail(request):
    return user_detail(request, request.user.pk)

class VendorListView(ListView):
    model = Vendor
    template_name = 'doors/vendor/list.html'

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        context['all_vendor_count'] = Vendor.objects.count()
        return context

class PlaceListView(ListView):
    model = Place
    template_name = 'doors/place/list.html'

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['all_place_count'] = Place.objects.count()
        return context
