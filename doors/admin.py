from django.contrib import admin
from mysite.doors.models import *

class LogAdmin( admin.ModelAdmin ) :
    list_display = ( 'id', 't_created', 'user', 'message' )

admin.site.register( Group    )
admin.site.register( Item     )
admin.site.register( ItemType )
admin.site.register( Location )
admin.site.register( Log     , LogAdmin )
admin.site.register( Order    )
admin.site.register( Property )
admin.site.register( User     )
admin.site.register( Vendor   )
