from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from doors.models import Order, Comment
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
    template_name = 'doors/orders/list.html'
    #paginate_by = 10

    def get_queryset(self):
        return get_viewable_order_list(self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['all_orders_count'] = Order.objects.count()
        return context

@login_required
def orders_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order not in get_viewable_order_list(request.user):
        messages.error(request, "You don't have permission to view order #{}!".format(pk))

        return HttpResponseRedirect(reverse('orders_list'))

    return render(request, 'doors/orders/detail.html', get_orders_detail_dictionary(order=order, user=request.user))

class SelfUserDetailView(DetailView):
    model = User
    template_name = 'doors/users/detail.html'
    context_object_name = 'user_object'

    def get_object(self):
        return self.request.user

@login_required
def orders_create(request):
    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()
        dictionary = get_orders_create_dictionary(user=request.user, POST_data=request.POST)

        form = dictionary['form']

        if form.is_valid():
            creator   = form.cleaned_data['creator']
            place     = form.cleaned_data['place']
            work_type = form.cleaned_data['work_type']
            comment   = form.cleaned_data['comment']

            new_order = Order.objects.create(
                creator=creator,
                place=place,
                work_type=work_type,
                comment=comment
            )

            messages.success(request, "Your order #{} had been created!".format(new_order.pk))
            logger.info("{user} created order #{pk}".format(user=request.user, pk=new_order.pk))

            return HttpResponseRedirect(reverse('orders_detail', kwargs={'pk': new_order.pk}))
    # Not POST.
    else:
        dictionary = get_orders_create_dictionary(user=request.user)
        if dictionary is None:
            # Messages called in get_orders_create_dictionary().
            return HttpResponseRedirect(reverse('orders_list'))

    return render(request, 'doors/orders/create.html', dictionary)

def comments_create(request, order_pk):
    #import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        order = Order.objects.get(pk=order_pk)
        user = request.user

        dictionary = get_orders_detail_dictionary(order=order, user=request.user, POST_data=request.POST)
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
            return render(request, 'doors/orders/detail.html', dictionary)

    return HttpResponseRedirect(reverse('orders_detail', kwargs={'pk': order_pk}))
