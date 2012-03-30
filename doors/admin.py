from django.contrib import admin
from doors.models import *

class DoorsGroupAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'comment',
        'created',
        'modified',
    )
    search_fields = ( 'name', )

class PlaceAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'place_type',
        'owner',
        'manager',
        'tenant_count',
        'address_line_one',
        'address_line_two',
        'city',
        'state',
        'zip_code',
        'website',
        'phone',
        'created',
        'modified',
    )
    list_filter = ( 'owner', 'manager', 'city', 'zip_code', 'state', )
    search_fields = ( 'name', 'owner', 'manager', 'address_line_one', )

class UserTypeAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', )

class UserProfileAdmin( admin.ModelAdmin ) :
    list_display = (
        'user',
        'doors_group',
        'place',
        'created',
        'modified',
    )
    list_filter = ( 'doors_group', 'place', )
    filter_horizontal = ( 'user_types', )
    search_fields = ( 'email', 'first_name', 'last_name', )

class VendorAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'email',
        'phone',
        'address_line_one',
        'address_line_two',
        'city',
        'state',
        'zip_code',
        'created',
        'modified',
    )
    list_filter = ( 'city', 'state', 'zip_code', )
    filter_horizontal = ( 'representatives', )
    search_fields = ( 'name', 'email', 'phone', 'address_line_one', )

class OrderAdmin( admin.ModelAdmin ) :
    list_display  = (
        'id',
        'creator',
        'approver',
        'action',
        'next_step',
        'comment_count',
        'created',
        'modified',
    )
    list_filter = (
        'creator',
        'approver',
        'created',
        'action',
        'first_appointment',
        'second_appointment',
        'work_done',
        'follow_up',
        'paid',
        'modified',
    )
    date_hierarchy = 'created'
    search_fields = ( 'creator', 'manager', 'comment', )

class LogAdmin( admin.ModelAdmin ) :
    list_display = (
        'id',
        'log_type',
        'created',
        'user',
        'message',
    )
    list_filter    = ( 'log_type', 'user', 'created', )
    date_hierarchy = 'created'
    search_fields  = ( 'message', )

admin.site.register( UserProfile , UserProfileAdmin  )
admin.site.register( UserType    , UserTypeAdmin     )
admin.site.register( Order       , OrderAdmin        )
admin.site.register( DoorsGroup  , DoorsGroupAdmin   )
admin.site.register( Place       , PlaceAdmin        )
admin.site.register( Vendor      , VendorAdmin       )
admin.site.register( Log         , LogAdmin          )
