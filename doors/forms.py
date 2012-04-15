from django.forms import ModelForm
from doors.models import Order

class OrderCreateForm(ModelForm):
    class Meta :
        model=Order
        fields=('work_type', 'comment',)