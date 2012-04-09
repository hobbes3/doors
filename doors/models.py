from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.comments.models import Comment

# Signals
from django.contrib.comments.signals import comment_was_posted
from doors.signals import comment_posted

comment_was_posted.connect( comment_posted )

# "property" is a Python function so I use the word "place" instead in codes.
# On the front-end, however, a location is always referred as a "property".
class Place( models.Model ) :
    def __unicode__( self ) :
        return self.name

    def tenant_count( self ) :
        return self.userprofile_set.count()

    PLACE_TYPE_CHOICES = (
        ( 's', 'single-family house (detached)' ),
        ( 'm', 'multi-family house'             ),
        ( 't', 'terrance house (townhouse)'     ),
        ( 'd', 'duplex, triplex, etc.'          ),
        ( 'c', 'condominium'                    ),
        ( 'a', 'apartment'                      ),
        ( 'o', 'office'                         ),
    )

    name             = models.CharField( max_length = 135 )
    place_type       = models.CharField( max_length = 1, choices = PLACE_TYPE_CHOICES, default = 's' )
    managers         = models.ManyToManyField( User, related_name = 'manager', limit_choices_to = { 'userprofile__user_types' : 'pm' } )
    owners           = models.ManyToManyField( User, related_name = 'owner'  , limit_choices_to = { 'userprofile__user_types' : 'po' }, null = True, blank = True )
    comment          = models.TextField( blank = True )
    address_line_one = models.CharField( max_length = 135 )
    address_line_two = models.CharField( max_length = 135, blank = True )
    city             = models.CharField( max_length = 135 )
    state            = models.CharField( max_length = 135 )
    zip_code         = models.CharField( max_length = 135 )
    website          = models.URLField( blank = True )
    phone            = models.CharField( max_length = 135, blank = True )
    list_publicly    = models.BooleanField( default = False )
    created          = models.DateTimeField( auto_now_add = True )
    modified         = models.DateTimeField( auto_now = True )

class UserType( models.Model ) :
    def __unicode__( self ) :
        return self.name

    def user_count( self ) :
        return self.userprofile_set.count()

    TYPE_CHOICES = (
        ( 'ad', 'administrator'    ), # 1
        ( 'mo', 'moderator'        ), # 2
        ( 'vi', 'viewer'           ), # 3
        ( 'pm', 'property manager' ), # 4
        ( 'po', 'property owner'   ), # 5
        ( 'vm', 'vendor manager'   ), # 6
        ( 've', 'vendor'           ), # 7
        ( 'te', 'tenant'           ), # 8
    )

    name     = models.CharField( max_length = 2, choices = TYPE_CHOICES )
    created  = models.DateTimeField( auto_now_add = True )
    modified = models.DateTimeField( auto_now = True )

class UserProfile( models.Model ) :
    def __unicode__( self ) :
        return "{username} - {full_name}".format(
            username  = self.user.username,
            full_name = self.user.get_full_name()
        )

    def has_user_types( self, user_types ) :
        return self.user_types.filter( name__in = user_types ).count()

    def comment_count( self ) :
        return Comment.objects.filter( user_id = self.user.pk ).count()

    PLACE_STATUS_CHOICES = (
        ( 'n', 'none'     ),
        ( 'p', 'pending'  ),
        ( 'a', 'approved' ),
        ( 'r', 'rejected' ),
    )

    user         = models.OneToOneField( User )
    user_types   = models.ManyToManyField( UserType, null = True, blank = True )
    comment      = models.TextField( blank = True )
    phone        = models.CharField( max_length = 135, blank = True )
    room         = models.CharField( max_length = 135, blank = True )
    floor        = models.CharField( max_length = 135, blank = True )
    building     = models.CharField( max_length = 135, blank = True )
    place        = models.ForeignKey( Place, null = True, blank = True )
    place_status = models.CharField( max_length = 1, choices = PLACE_STATUS_CHOICES, default = 'n' )
    created      = models.DateTimeField( auto_now_add = True )
    modified     = models.DateTimeField( auto_now = True )

# Access UserProfile with User.profile, instead of User.get_profile().
# Also creates a UserProfile for a User if it doens't exist already.
User.profile = property( lambda u : UserProfile.objects.get_or_create( user = u )[ 0 ] )

# Also don't forget to add
# AUTH_PROFILE_MODULE = "doors.UserProfile"
# in the project's setting.py.

class Vendor( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name             = models.CharField( max_length = 135 )
    comment          = models.TextField( blank = True )
    phone            = models.CharField( max_length = 135, blank = True )
    email            = models.EmailField( blank = True )
    website          = models.URLField( blank = True )
    address_line_one = models.CharField( max_length = 135 )
    address_line_two = models.CharField( max_length = 135, blank = True )
    city             = models.CharField( max_length = 135 )
    state            = models.CharField( max_length = 135 )
    zip_code         = models.CharField( max_length = 135 )
    managers         = models.ManyToManyField( User, related_name = 'managers'       , limit_choices_to = { 'userprofile__user_types' : 'vm' } )
    representatives  = models.ManyToManyField( User, related_name = 'representatives', limit_choices_to = { 'userprofile__user_types' : 've' }, null = True, blank = True )
    created          = models.DateTimeField( auto_now_add = True )
    modified         = models.DateTimeField( auto_now = True )

class Order( models.Model ) :
    def __unicode__( self ) :
        return unicode( self.pk )

    # For permalinking comments.
    def get_absolute_url( self ) :
        return reverse( 'orders_detail', kwargs = { 'pk' : self.pk } )

    def comment_count( self ) :
        content_type = ContentType.objects.get_for_model( Order )
        object_pk = self.pk
        return Comment.objects.filter( content_type = content_type, object_pk = object_pk ).count()

    def all_steps( self ) :
        user = self.creator.first_name

        return [
            ( getattr( self, attr ), task.format( user = user ) )
            for ( attr, task ) in self.TASKS
        ]

    def next_step( self ) :
        user = self.creator.first_name

        task_num = next(
            ( i for ( i, ( attr, task ) ) in enumerate( self.TASKS ) if getattr( self, attr ) is None ),
            None
        )

        if task_num == None :
            return "Done!"
        else:
            return "{number}: {task}".format(
                number = str( task_num + 1 ),
                task   = self.TASKS[ task_num ][ 1 ].format( user = user )
            )

    TASKS = (
        ( 'action'            , "Review, then either approve or reject the order." ),
        ( 'first_appointment' , "Contact a vendor to get a quote and arrange an appointment for {user}." ),
        ( 'second_appointment', "Review the quote, (get owner approval), then arrange a second appointment for the repairs." ),
        ( 'work_done'         , "Confirm the finished repairs and pay the vendor." ),
        ( 'follow_up'         , "Follow up with {user}." ),
        ( 'paid'              , "Confirm payment and close the order." ),
    )

    STATUS_CHOICES = (
        ( 'p', 'pending'  ),
        ( 'a', 'approved' ),
        ( 'r', 'rejected' ),
        ( 'c', 'closed'   ),
        ( 'l', 'locked'   ),
    )

    WORK_TYPE_CHOICES = (
        ( 'hc', 'Heating and cooling' ),
        ( 'el', 'Electrical'          ),
        ( 'pl', 'Plumbing'            ),
        ( 'ap', 'Appliances'          ),
        ( 'pe', 'Pests'               ),
        ( 'ex', 'Exterior'            ),
        ( 'in', 'Interior'            ),
        ( 'sa', 'Safety'              ),
        ( 'ot', 'Others'              ),
    )

    creator   = models.ForeignKey( User, related_name = 'creator' )
    approver  = models.ForeignKey( User, related_name = 'approver' )
    comment   = models.TextField( blank = True )
    status    = models.CharField( max_length = 1, choices = STATUS_CHOICES, default = 'p' )
    quote     = models.DecimalField( max_digits = 8, decimal_places = 2, null = True, blank = True )
    payment   = models.DecimalField( max_digits = 8, decimal_places = 2, null = True, blank = True )
    work_type = models.CharField( max_length = 2, choices = WORK_TYPE_CHOICES )
    vendor    = models.ForeignKey( Vendor, null = True, blank = True )
    place     = models.ForeignKey( Place )

    created            = models.DateTimeField( auto_now_add = True )
    action             = models.DateTimeField( null = True, blank = True )
    first_appointment  = models.DateTimeField( null = True, blank = True )
    second_appointment = models.DateTimeField( null = True, blank = True )
    work_done          = models.DateTimeField( null = True, blank = True )
    follow_up          = models.DateTimeField( null = True, blank = True, verbose_name = 'follow-up' )
    paid               = models.DateTimeField( null = True, blank = True )
    modified           = models.DateTimeField( auto_now = True )
