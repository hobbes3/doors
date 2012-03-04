from django.contrib import admin
from mysite.doors.models import *

class GroupAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        't_created',
        't_modified',
    )
    search_fields = ( 'name', )

class ItemAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'comment',
        'item_type',
        'location',
        't_created',
        't_modified',
    )
    list_filter = ( 'item_type', )
    search_fields = ( 'name', 'comment', )

class ItemTypeAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'comment',
        't_created',
        't_modified',
    )
    filter_horizontal = ( 'vendors', )
    search_fields = ( 'name', 'comment', )

class LocationAdmin( admin.ModelAdmin ) :
    list_display = (
        'comment',
        'room',
        'floor',
        'building',
        'prop',
        't_created',
        't_modified',
    )
    list_filter = ( 'prop', )
    search_fields = ( 'comment', 'prop', )

class OrderAdmin( admin.ModelAdmin ) :
    list_display  = (
        'id',
        'user_created',
        'action',
        'next_step',
        't_created',
        't_modified',
    )
    filter_horizontal = ( 'items', )
    list_filter = (
        'user_created',
        'user_action',
        't_created',
        't_action',
        't_followup_one',
        't_vendor_appt_one',
        't_vendor_appt_two',
        't_work_done',
        't_followup_two',
        't_paid',
    )
    date_hierarchy = 't_created'
    search_fields = ( 'user_created', 'user_action', )

class OrderCommentAdmin( admin.ModelAdmin ) :
    list_display = (
        'order',
        'user',
        'comment',
        'status',
        't_created',
        't_modified',
    )
    list_filter = ( 'order', )
    date_hierarchy = 't_created'
    search_fields = ( 'order', 'user', 'comment', )

class LogAdmin( admin.ModelAdmin ) :
    list_display = (
        'id',
        'log_type',
        't_created',
        'user',
        'message',
    )
    list_filter    = ( 'log_type', 'user', 't_created', )
    date_hierarchy = 't_created'
    search_fields  = ( 'message', )

class PropertyAdmin( admin.ModelAdmin ) :
    list_display = (
        'name',
        'owner',
        'address_line_one',
        'address_line_two',
        'city',
        'state',
        'zip_code',
        't_created',
        't_modified',
    )
    list_filter = ( 'owner', 'city', 'zip_code', 'state', )
    search_fields = ( 'name', 'owner', 'address_line_one', )

class UserAdmin( admin.ModelAdmin ) :
    list_display = (
        'email',
        'group',
        'first_name',
        'last_name',
        'user_type',
        'status',
        'location',
        't_created',
        't_modified',
    )
    list_filter = ( 'group', 'location', )
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
        't_created',
        't_modified',
    )
    list_filter = ( 'city', 'state', 'zip_code', )
    search_fields = ( 'name', 'email', 'phone', 'address_line_one', )

admin.site.register( Group       , GroupAdmin        )
admin.site.register( Item        , ItemAdmin         )
admin.site.register( ItemType    , ItemTypeAdmin     )
admin.site.register( Location    , LocationAdmin     )
admin.site.register( Log         , LogAdmin          )
admin.site.register( Order       , OrderAdmin        )
admin.site.register( OrderComment, OrderCommentAdmin )
admin.site.register( Property    , PropertyAdmin     )
admin.site.register( User        , UserAdmin         )
admin.site.register( Vendor      , VendorAdmin       )
