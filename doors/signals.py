from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)

def comment_posted(sender, comment=None, request=None, **kwargs):
    messages.add_message(request, messages.SUCCESS, "You comment has been posted!")
    logger.info("{user} created comment #{comment_pk} for order #{order_pk}".format(
        user      =request.user,
        comment_pk=comment.pk,
        order_pk  =comment.object_pk
    ))
    logger.info("comment: {}".format(comment.comment))
