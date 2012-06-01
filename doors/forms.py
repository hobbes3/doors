import datetime
from django import forms
from django.db.models.query import EmptyQuerySet
from doors.models import Order, Property, Vendor

class CustomDateTimeField(forms.DateTimeField):
    def strptime(self, value, format):
        return datetime.datetime.strptime(value.replace('a.m.', 'AM').replace('p.m.', 'PM'), '%B %d, %Y, %I:%M %p')

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class OrderCreateForm(forms.Form):
    work_type = forms.ChoiceField(choices=Order.WORK_TYPE_CHOICES)
    note = forms.CharField(widget=forms.Textarea)

    def __init__(self, creator_list=None, property_list=None, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        if creator_list:
            self.fields['creator'] = UserModelChoiceField(
                queryset=creator_list,
                empty_label="Select a user",
            )

        if property_list:
            self.fields['property'] = forms.ModelChoiceField(
                queryset=property_list,
                empty_label=None,
            )
        else:
            self.fields['property'] = forms.ModelChoiceField(
                queryset=EmptyQuerySet(),
                empty_label="Select a creator first",
            )

    def clean(self):
        super(OrderCreateForm, self).clean()

        if 'note' in self.cleaned_data:
            if len(self.cleaned_data['note']) < 20:
                self._errors['note'] = self.error_class([u"Please enter a longer note."])

                del self.cleaned_data['note']

        return self.cleaned_data

class CommentCreateForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

    def clean(self):
        super(CommentCreateForm, self).clean()

        if 'comment' in self.cleaned_data:
            if len(self.cleaned_data['comment']) < 10:
                self._errors['comment'] = self.error_class([u"Please enter a longer comment."])

                del self.cleaned_data['comment']

        return self.cleaned_data

def make_order_edit_form(include_fields):
    class _OrderEditForm(forms.ModelForm):
        if 'fa_date' in include_fields:
            fa_date = CustomDateTimeField(label="first appointment time")
        if 'sa_date' in include_fields:
            sa_date = CustomDateTimeField(label="second appointment time")

        class Meta:
            model = Order
            fields = include_fields
            widgets = {
                'status':                forms.RadioSelect(),
                'fa_status_creator':     forms.RadioSelect(),
                'fa_status_vendor':      forms.RadioSelect(),
                'quote_status_approver': forms.RadioSelect(),
                'quote_status_owner':    forms.RadioSelect(),
                'sa_status_creator':     forms.RadioSelect(),
                'sa_status_vendor':      forms.RadioSelect(),
            }

        def clean(self):
            super(_OrderEditForm, self).clean()

            if 'note' in self.cleaned_data:
                if len(self.cleaned_data['note']) < 20:
                    self._errors['note'] = self.error_class([u"Please enter a longer note."])

                    del self.cleaned_data['note']

            return self.cleaned_data

    return _OrderEditForm
