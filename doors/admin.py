from django.contrib import admin
from mysite.doors.models import *

class GroupAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', 't_created', 't_modified', )

class ItemAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', 'comment', 'item_type', 'location', 't_created', 't_modified', )

class ItemTypeAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', 'comment', 't_created', 't_modified', )
    filter_horizontal = ( 'vendors', )

class LocationAdmin( admin.ModelAdmin ) :
    list_display = ( 'comment', 'room', 'floor', 'building', 'prop', 't_created', 't_modified' )

class OrderAdmin( admin.ModelAdmin ) :
    list_display  = ( 'id', 't_created', 't_modified', 'user_created', 'comment', 'status', )
    filter_horizontal = ( 'items', )
    list_filter = ( 'user_created', 'user_status', 't_created', 't_status' )

class LogAdmin( admin.ModelAdmin ) :
    list_display   = ( 'id', 'log_type', 't_created', 'user', 'message', )
    search_fields  = ( 'message', )
    list_filter    = ( 'user', 't_created', )
    date_hierarchy = 't_created'

class PropertyAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', 'owner', 'address_line_one', 'address_line_two', 'city', 'state', 'zip_code', 't_created', 't_modified', )

class UserAdmin( admin.ModelAdmin ) :
    list_display = ( 'email', 'group', 'first_name', 'last_name', 'user_type', 'status', 'location', 't_created', 't_modified', )
    search_fields = ( 'email', 'first_name', 'last_name', )

class VendorAdmin( admin.ModelAdmin ) :
    list_display = ( 'name', 'email', 'phone', 'address_line_one', 'address_line_two', 'city', 'state', 'zip_code', 't_created', 't_modified', )

admin.site.register( Group   , GroupAdmin    )
admin.site.register( Item    , ItemAdmin     )
admin.site.register( ItemType, ItemTypeAdmin )
admin.site.register( Location, LocationAdmin )
admin.site.register( Log     , LogAdmin      )
admin.site.register( Order   , OrderAdmin    )
admin.site.register( Property, PropertyAdmin )
admin.site.register( User    , UserAdmin     )
admin.site.register( Vendor  , VendorAdmin   )
