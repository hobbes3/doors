from django.contrib import messages
from django.utils import simplejson, timezone, dateformat
from dajaxice.decorators import dajaxice_register
from doors.models import Order
from pytz import timezone as pytz_timezone

@dajaxice_register
def step_changed(request, order_pk, local_timezone, step_pk, checked):
    order = Order.objects.get(pk=order_pk)
    disabled_steps = order.disabled_steps()

    #import ipdb; ipdb.set_trace()

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
