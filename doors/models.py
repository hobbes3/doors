from django.db import models

class Group( models.Model ) :
    def __unicode__( self ) :
        return self.name

    P_CHOICES = (
        ( 'n', 'none'           ),
        ( 'r', 'read only'      ),
        ( 'w', 'read and write' ),
    )

    name            = models.CharField( max_length = 135 )
    comment         = models.TextField( blank = True )
    p_group         = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_user          = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_order_self    = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_order_other   = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_comment_self  = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_comment_other = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_item_type     = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_item          = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_property      = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_location      = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_vendor        = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    t_created       = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified      = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Vendor( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name              = models.CharField( max_length = 135 )
    comment           = models.TextField( blank = True )
    phone             = models.CharField( max_length = 135, blank = True )
    email             = models.EmailField( blank = True )
    website           = models.URLField( blank = True )
    address_line_one  = models.CharField( max_length = 135 )
    address_line_two  = models.CharField( max_length = 135, blank = True )
    city              = models.CharField( max_length = 135 )
    state             = models.CharField( max_length = 135 )
    zip_code          = models.CharField( max_length = 135 )
    t_created         = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified        = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class ItemType( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name       = models.CharField( max_length = 135 )
    comment    = models.TextField( blank = True )
    vendors    = models.ManyToManyField( Vendor )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class User( models.Model ) :
    def __unicode__( self ) :
        return self.first_name + " " + self.last_name

    TYPE_CHOICES = (
        ( 't', 'tenant'           ),
        ( 'o', 'property owner'   ),
        ( 'v', 'vendor'           ),
        ( 'm', 'property manager' ),
        ( 'w', 'web user'         ),
    )

    STATUS_CHOICES = (
        ( 'p', 'pending'  ),
        ( 'a', 'active'   ),
        ( 'i', 'inactive' ),
        ( 'b', 'banned'   ),
    )

    email      = models.EmailField()
    group      = models.ForeignKey( Group )
    user_type  = models.CharField( max_length = 1, choices = TYPE_CHOICES, default = 't' )
    comment    = models.TextField( blank = True )
    password   = models.CharField( max_length = 135 )
    first_name = models.CharField( max_length = 135 )
    last_name  = models.CharField( max_length = 135 )
    phone      = models.CharField( max_length = 135, blank = True )
    status     = models.CharField( max_length = 1, choices = STATUS_CHOICES, default = 'p' )
    location   = models.ForeignKey( 'Location', null = True, blank = True )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Property( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name             = models.CharField( max_length = 135 )
    owner            = models.ForeignKey( User )
    comment          = models.TextField( blank = True )
    address_line_one = models.CharField( max_length = 135 )
    address_line_two = models.CharField( max_length = 135, blank = True )
    city             = models.CharField( max_length = 135 )
    state            = models.CharField( max_length = 135 )
    zip_code         = models.CharField( max_length = 135 )
    t_created        = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified       = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

    class Meta:
         verbose_name_plural = "properties"

class Location( models.Model ) :
    def __unicode__( self ) :
        locations = filter( None, [ self.room, self.floor, self.building ] )
        locations.append( self.prop.__unicode__() )

        return ", ".join( locations )

    comment    = models.TextField( blank = True )
    room       = models.CharField( max_length = 135, blank = True )
    floor      = models.CharField( max_length = 135, blank = True )
    building   = models.CharField( max_length = 135, blank = True )
    prop       = models.ForeignKey( Property )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Item( models.Model ) :
    def __unicode__( self ) :
        return self.name + " : " + self.location.__unicode__()

    name       = models.CharField( max_length = 135 )
    comment    = models.TextField( blank = True )
    item_type  = models.ForeignKey( ItemType )
    location   = models.ForeignKey( Location )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Order( models.Model ) :
    def __unicode__( self ) :
        return str( self.id )

    def next_step( self ) :
        user = self.user_created.first_name

        if self.t_action is None :
            return "1: Review, then either approve or reject the order."
        elif self.t_followup is None :
            return "2: Follow up with " + user + "."
        elif self.t_vendor_appt_one is None :
            return "3: Contact the vendor to get a quote and arrange an appointment for " + user + "."
        elif self.t_vendor_appt_two is None :
            return "4: Review the quote, (get owner approval), then arrange a second appointment for the repairs."
        elif self.t_work_done is None :
            return "5: Confirm that the work is done and pay the vendor."
        elif self.t_followup_two is None :
            return "6: Follow up again with " + user + "."
        elif self.paid is None :
            return "7: Confirm payment and close the order."

    ACTION_CHOICES = (
        ( 'p', 'pending'  ),
        ( 'a', 'approved' ),
        ( 'r', 'rejected' ),
        ( 'c', 'closed'   ),
    )

    user_created      = models.ForeignKey( User, related_name = 'user_created' )
    t_created         = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_action          = models.DateTimeField( null = True, blank = True, verbose_name = 'action'             )
    t_followup_one    = models.DateTimeField( null = True, blank = True, verbose_name = 'first follow-up'    )
    t_vendor_appt_one = models.DateTimeField( null = True, blank = True, verbose_name = 'first appointment'  )
    t_vendor_appt_two = models.DateTimeField( null = True, blank = True, verbose_name = 'second appointment' )
    t_work_done       = models.DateTimeField( null = True, blank = True, verbose_name = 'work done'          )
    t_followup_two    = models.DateTimeField( null = True, blank = True, verbose_name = 'second follow-up'   )
    t_paid            = models.DateTimeField( null = True, blank = True, verbose_name = 'paid'               )
    action            = models.CharField( max_length = 1, choices = ACTION_CHOICES, default = 'p' )
    user_action       = models.ForeignKey( User, related_name = 'user_status', null = True, blank = True )
    quote             = models.DecimalField( max_digits = 8, decimal_places = 2, null = True, blank = True )
    payment           = models.DecimalField( max_digits = 8, decimal_places = 2, null = True, blank = True )
    items             = models.ManyToManyField( Item, null = True, blank = True )
    t_modified        = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class OrderComment( models.Model ) :
    def __unicode__( self ) :
        return self.order.id

    STATUS_CHOICES = (
        ( 'v', 'visible' ),
        ( 'd', 'deleted' ),
    )

    order      = models.ForeignKey( Order )
    user       = models.ForeignKey( User )
    comment    = models.TextField()
    status     = models.CharField( max_length = 1, choices = STATUS_CHOICES, default = 'v' )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Log( models.Model ) :
    def __unicode__( self ) :
        return str( self.id )

    class Meta :
        ordering = [ 't_created' ]

    TYPE_CHOICES = (
        ( 'i', 'info'    ),
        ( 'w', 'warning' ),
        ( 'e', 'error'   ),
    )

    user      = models.ForeignKey( User )
    log_type  = models.CharField( max_length = 1, choices = TYPE_CHOICES, default = 'i' )
    message   = models.CharField( max_length = 500 )
    t_created = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
