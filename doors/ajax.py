from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import simplejson, timezone, dateformat
from dajaxice.decorators import dajaxice_register
from doors.models import Order, Comment
from pytz import timezone as pytz_timezone

@dajaxice_register
def order_detail_step_changed(request, order_pk, local_timezone, step_pk, checked):
    #import ipdb; ipdb.set_trace()

    order = Order.objects.get(pk=order_pk)
    disabled_steps = order.disabled_steps()

    if step_pk in disabled_steps:
        messages.error(request, "Something went wrong! You weren't suppose to be able to {} that step!".format('check' if checked else 'uncheck'))
        return simplejson.dumps({'error': True})

    # timezone.now() is in UTC.
    current_time = timezone.now()

    # The first step is STEPS[0].
    attr, code, task = order.STEPS[step_pk - 1]

    setattr(order, attr, current_time if checked else None)
    order.save()

    new_comment = Comment(order=order, action_type=code, created=current_time)
    new_comment.comment = new_comment.get_action_type_description(code).format(user=request.user.get_full_name(), action="checked" if checked else "unchecked")
    new_comment.save()

    # Convert current_time to the local time depending on the local_timezone.
    local_current_time = current_time.astimezone(pytz_timezone(local_timezone))
    # dateformat.format() formats the time as Django would format it in the template. Displaying time format like 'midnight' and '6 pm' (as oppose to '6:00' pm).
    formatted_local_current_time = dateformat.format(local_current_time, 'F j, Y, P')

    return simplejson.dumps({
        'error': False,
        'checked': checked,
        'disabled_steps': order.disabled_steps(),
        'total_steps': order.total_steps(),
        'step_pk': step_pk,
        'datetime': formatted_local_current_time,
        'user': request.user.get_full_name(),
        'comment_pk': new_comment.pk,
        'comment': new_comment.comment
    })

@dajaxice_register
def order_create_creator_changed(request, creator_pk):
    #import ipdb; ipdb.set_trace()

    # Check for empty string (if "Select a user" was selected).
    if not creator_pk:
        return simplejson.dumps({
            'error': False,
            'properties': [('', "Select a creator first")]
        })
    else:
        creator_pk = int(creator_pk)

    creator = User.objects.get(pk=creator_pk)

    if creator.profile.has_user_types(['pm']):
        properties = [(property.pk, property.name) for property in creator.properties_from_managers.all()]
    elif creator.profile.has_user_types(['te']):
        property = creator.profile.property
        if property:
            properties = [(property.pk, property.name)]
        else:
            properties = [('', "Creator is not part of a property")]
    else:
        messages.error(request, "Something went wrong! The creator is suppose to be either a tenant or a property manager!")
        return simplejson.dumps({'error': True})

    return simplejson.dumps({
        'error': False,
        'properties': properties
    })
