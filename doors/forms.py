from django import forms
from django.db.models.query import EmptyQuerySet
from doors.models import Order, Place

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class OrderCreateForm(forms.Form):
    work_type = forms.ChoiceField(choices=Order.WORK_TYPE_CHOICES)
    comment = forms.CharField(widget=forms.Textarea)

    def __init__(self, creator_list=None, place_list=None, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        if creator_list:
            self.fields['creator'] = UserModelChoiceField(
                queryset=creator_list,
                empty_label="Select a user"
            )

        if place_list:
            self.fields['place'] = forms.ModelChoiceField(
                queryset=place_list,
                empty_label=None
            )
        else:
            self.fields['place'] = forms.ModelChoiceField(
                queryset=EmptyQuerySet(),
                empty_label="Select a creator first"
            )

    def clean(self):
        super(OrderCreateForm, self).clean()

        if 'comment' in self.cleaned_data:
            if len(self.cleaned_data['comment']) < 50:
                self._errors['comment'] = self.error_class([u"Please enter a longer comment."])

                del self.cleaned_data['comment']

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
