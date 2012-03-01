from django.contrib import admin
from mysite.doors.models import *

class OrderAdmin( admin.ModelAdmin ) :
    filter_horizontal = ( 'items', )

class LogAdmin( admin.ModelAdmin ) :
    list_display  = ( 'id', 't_created', 'user', 'message', )
    search_fields = ( 'message', )
    list_filter   = ( 'user', 't_created', )
    date_hierarchy = 't_created'

admin.site.register( Group    )
admin.site.register( Item     )
admin.site.register( ItemType )
admin.site.register( Location )
admin.site.register( Log     , LogAdmin   )
admin.site.register( Order   , OrderAdmin )
admin.site.register( Property )
admin.site.register( User     )
admin.site.register( Vendor   )
