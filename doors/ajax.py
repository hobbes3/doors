from django.contrib import messages
from django.utils import simplejson, timezone, dateformat
from dajaxice.decorators import dajaxice_register
from doors.models import Order
from django.contrib.auth.models import User
from pytz import timezone as pytz_timezone

@dajaxice_register
def orders_detail_step_changed(request, order_pk, local_timezone, step_pk, checked):
    order = Order.objects.get(pk=order_pk)
    disabled_steps = order.disabled_steps()

    if step_pk in disabled_steps:
        messages.error(request, "Something went wrong! You weren't suppose to be able to {} that step!".format('check' if checked else 'uncheck'))
        return simplejson.dumps({'error': True})

    # timezone.now() is in UTC.
    current_time = timezone.now() if checked else None

    # The first step is STEPS[0].
    setattr(order, order.STEPS[step_pk - 1][0], current_time)
    order.save()

    # Convert current_time to the local time depending on the local_timezone.
    local_current_time = current_time.astimezone(pytz_timezone(local_timezone)) if checked else None

    return simplejson.dumps({
        'error': False,
        'disabled_steps': order.disabled_steps(),
        'total_steps': order.total_steps(),
        'step_pk': step_pk,
        # dateformat() formats local_current_time as Django would format it in the template.
        'datetime': dateformat.format(local_current_time, 'F j, Y, P') if checked else 'None'
    })

@dajaxice_register
def orders_create_creator_changed(request, creator_pk):
    #import ipdb; ipdb.set_trace()

    # Check for empty string (if "Select a user" was selected).
    if not creator_pk:
        return simplejson.dumps({
            'error': False,
            'places': [('', "Select a creator first")]
        })
    else:
        creator_pk = int(creator_pk)

    creator = User.objects.get(pk=creator_pk)

    if creator.profile.has_user_types(['pm']):
        places = [(place.pk, place.name) for place in creator.place_managers.all()]
    elif creator.profile.has_user_types(['te']):
        place = creator.profile.place
        if place:
            places = [(place.pk, place.name)]
        else:
            places = [('', "Creator is not part of a property")]
    else:
        messages.error(request, "Something went wrong! The creator is suppose to be either a tenant or a property manager!")
        return simplejson.dumps({'error': True})

    return simplejson.dumps({
        'error': False,
        'places': places
    })
