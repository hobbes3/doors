from django.forms import ModelForm, ModelChoiceField, Select
from django.db.models.query import EmptyQuerySet
from doors.models import Order, Place

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class OrderCreateForm(ModelForm):
    class Meta:
        model=Order
        fields=('work_type', 'comment',)

    def __init__(self, creator_list=None, place_list=None, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        if creator_list:
            self.fields['creator'] = UserModelChoiceField(
                queryset=creator_list,
                empty_label="Select a user",
                widget=Select(attrs={
                    'onchange': "Dajaxice.doors.orders_create_creator_changed(fill_other_fields, {'creator_pk': this.options[this.selectedIndex].value})"
                })
            )

        if place_list:
            self.fields['place'] = ModelChoiceField(
                queryset=place_list,
                empty_label=None
            )
        else:
            self.fields['place'] = ModelChoiceField(
                queryset=EmptyQuerySet(),
                empty_label="Select a creator first"
            )
