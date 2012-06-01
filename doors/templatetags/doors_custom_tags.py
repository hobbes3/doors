from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def duration(value):
    hours   = value / 60
    minutes = value % 60

    hours_string   = str(hours)   + (" hours"   if hours   > 1 else " hour"  ) if hours   else ""
    minutes_string = str(minutes) + (" minutes" if minutes > 1 else " minute") if minutes else ""

    return ' '.join("{hours} {minutes}".format(hours=hours_string, minutes=minutes_string).split())

@register.filter
def has_user_types(element, args):
    if isinstance(element, User):
        user_types = args.replace(' ', '').split(',')

        if element.profile.has_user_types(user_types):
            return True

    return False

@register.filter
def class_name(element):
    return element.__class__.__name__

@register.filter
def pdb(element):
    import pdb; pdb.set_trace()
    return element
