from django.forms import ModelForm
from doors.models import Order

class OrderCreateForm( ModelForm ) :
    class Meta :
        model = Order
        fields = (
            'creator',
            'approver',
            'work_type',
            'comment',
        )
