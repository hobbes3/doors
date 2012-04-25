from django.contrib import admin
from doors.models import *

class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'place_type',
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
    list_filter = ('owners', 'managers', 'city', 'zip_code', 'state',)
    search_fields = ('name', 'owners', 'managers', 'address_line_one',)
    filter_horizontal = ('owners', 'managers',)

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'place',
        'comment_count',
        'created',
        'modified',
    )
    list_filter = ('place',)
    filter_horizontal = ('user_types',)
    search_fields = ('email', 'first_name', 'last_name',)

class VendorAdmin(admin.ModelAdmin):
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
    list_filter = ('city', 'state', 'zip_code',)
    filter_horizontal = ('managers', 'representatives',)
    search_fields = ('name', 'email', 'phone', 'address_line_one',)

class OrderAdmin(admin.ModelAdmin):
    list_display  = (
        'id',
        'creator',
        'approver',
        'place',
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
    search_fields = ('place', 'creator', 'manager', 'comment',)

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'user',
        'action_type',
        'comment',
        'created',
        'modified',
    )
    list_filter = ('order', 'user', 'action_type',)
    search_fields = ('order', 'user', 'comment',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserType   , UserTypeAdmin   )
admin.site.register(Order      , OrderAdmin      )
admin.site.register(Comment    , CommentAdmin    )
admin.site.register(Place      , PlaceAdmin      )
admin.site.register(Vendor     , VendorAdmin     )
