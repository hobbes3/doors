from django.forms import ModelForm, ModelChoiceField, Select
from doors.models import Order
from django.contrib.auth.models import User

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class OrderCreateForm(ModelForm):
    class Meta:
        model=Order
        fields=('work_type', 'comment',)

    def __init__(self, creator_list=None, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        if creator_list:
            self.fields['creator'] = UserModelChoiceField(
                queryset=creator_list,
                empty_label="Select a user",
                widget=Select(attrs={
                    'onchange': "Dajaxice.doors.orders_create_creator_changed(fill_other_fields, {'creator_pk': this.options[this.selectedIndex].value})"
                })
            )

        self.fields['place'] = UserModelChoiceField(
            queryset=User.objects.none(),
            empty_label="Select a creator first"
        )
