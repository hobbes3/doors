from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)

def add_can_view( sender, **kwargs ) :
    logger.debug( "===add_can_view===" )
    logger.debug( "sender = {}".format( sender ) )

    for content_type in ContentType.objects.all():
        logger.debug( "model = {}".format( content_type.model ) )
        logger.debug( "pk = {}".format( content_type.pk ) )

        if Permission.objects.filter(
            content_type_id = content_type.pk,
            codename__contains = 'view_'
        ) is None :
            content_type_pks.append( content_type.pk )

            logger.debug( "adding view permission..." )

            Permission.objects.create(
                content_type = content_type,
                codename     = 'view_{}'.format( content_type.model ),
                name         = 'Can view {}'.format( content_type.name )
            )

def comment_posted( sender, comment = None, request = None, **kwargs ) :
    messages.add_message( request, messages.SUCCESS, "You comment has been posted!" )
