from django.db import models

class Group( models.Model ) :
    def __unicode__( self ) :
        return self.name

    P_CHOICES = (
        ( 'n', 'none'           ),
        ( 'r', 'read only'      ),
        ( 'w', 'read and write' ),
    )

    name          = models.CharField( max_length = 135 )
    comment       = models.TextField( blank = True )
    p_group       = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_user        = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_order_self  = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_order_other = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_item_type   = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_item        = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_property    = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_location    = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    p_vendor      = models.CharField( max_length = 1, choices = P_CHOICES, default = 'n' )
    t_created     = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified    = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Vendor( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name              = models.CharField( max_length = 135 )
    comment           = models.TextField( blank = True )
    phone             = models.CharField( max_length = 135, blank = True )
    email             = models.CharField( max_length = 135, blank = True )
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

class Property( models.Model ) :
    def __unicode__( self ) :
        return self.name

    name             = models.CharField( max_length = 135 )
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

class User( models.Model ) :
    def __unicode__( self ) :
        return self.first_name + " " + self.last_name

    STATUS_CHOICES = (
        ( 'p', 'pending'  ),
        ( 'a', 'active'   ),
        ( 'i', 'inactive' ),
        ( 'b', 'banned'   ),
    )

    group      = models.ForeignKey( Group )
    comment    = models.TextField( blank = True )
    email      = models.CharField( max_length = 135 )
    password   = models.CharField( max_length = 135 )
    first_name = models.CharField( max_length = 135 )
    last_name  = models.CharField( max_length = 135 )
    phone      = models.CharField( max_length = 135, blank = True )
    status     = models.CharField( max_length = 1, choices = STATUS_CHOICES, default = 'p' )
    location   = models.ForeignKey( Location, null = True, blank = True )
    t_created  = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Order( models.Model ) :
    def __unicode__( self ) :
        return str( self.id )

    STATUS_CHOICES = (
        ( 'p', 'pending'  ),
        ( 'a', 'approved' ),
        ( 'r', 'rejected' ),
    )

    order_previous = models.ForeignKey( 'self', null = True, blank = True )
    user_created   = models.ForeignKey( User, related_name = 'user_created' )
    user_modified  = models.ForeignKey( User, related_name = 'user_modified', null = True, blank = True )
    items          = models.ManyToManyField( Item )
    comment        = models.TextField( blank = True )
    status         = models.CharField( max_length = 1, choices = STATUS_CHOICES, default = 'p' )
    t_status       = models.DateTimeField( null = True, blank = True )
    user_status    = models.ForeignKey( User, related_name = 'user_status', null = True, blank = True )
    t_created      = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
    t_modified     = models.DateTimeField( auto_now = True, verbose_name = 'modified' )

class Log( models.Model ) :
    def __unicode__( self ) :
        return str( self.id )

    class Meta :
        ordering = [ 't_created' ]

    user      = models.ForeignKey( User )
    message   = models.CharField( max_length = 500 )
    t_created = models.DateTimeField( auto_now_add = True, verbose_name = 'created' )
