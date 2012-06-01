from django.contrib import admin
from doors.models import *

class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'property_type',
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
        'property',
        'comment_count',
        'created',
        'modified',
    )
    list_filter = ('property',)
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
        'property',
        'action',
        'quote',
        'payment',
        'next_step',
        'comment_count',
        'created',
        'modified',
    )
    list_filter = (
        'creator',
        'approver',
        'created',
        'assigned_approver',
        'action',
        'assigned_vendor',
        'first_appointment',
        'quoted',
        'second_appointment',
        'work_done',
        'followed_up',
        'paid',
        'modified',
    )
    date_hierarchy = 'created'
    search_fields = ('property', 'creator', 'manager', 'comment',)

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
admin.site.register(Property   , PropertyAdmin   )
admin.site.register(Vendor     , VendorAdmin     )
