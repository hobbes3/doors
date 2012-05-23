from django import forms
from django.db.models.query import EmptyQuerySet
from doors.models import Order, Place, Vendor

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class OrderCreateForm(forms.Form):
    work_type = forms.ChoiceField(choices=Order.WORK_TYPE_CHOICES)
    note = forms.CharField(widget=forms.Textarea)

    def __init__(self, creator_list=None, place_list=None, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        if creator_list:
            self.fields['creator'] = UserModelChoiceField(
                queryset=creator_list,
                empty_label="Select a user",
            )

        if place_list:
            self.fields['place'] = forms.ModelChoiceField(
                queryset=place_list,
                empty_label=None,
            )
        else:
            self.fields['place'] = forms.ModelChoiceField(
                queryset=EmptyQuerySet(),
                empty_label="Select a creator first",
            )

    def clean(self):
        super(OrderCreateForm, self).clean()

        if 'note' in self.cleaned_data:
            if len(self.cleaned_data['note']) < 50:
                self._errors['note'] = self.error_class([u"Please enter a longer note."])

                del self.cleaned_data['note']

        return self.cleaned_data

class OrderDetailForm(forms.Form):
    def __init__(
        self,
        user,
        order,
        can_edit_work_type=None,
        can_edit_vendor=None,
        can_edit_note=None,
        can_edit_status=None,
        can_edit_quote=None,
        can_edit_payment=None,
        can_edit_fa_date=None,
        can_edit_sa_date=None,
        can_edit_fa_duration=None,
        can_edit_sa_duration=None,
        can_accept_fa=None,
        can_accept_sa=None,
        can_accept_quote=None,
        *args,
        **kwargs
    ):
        super(OrderDetailForm, self).__init__(*args, **kwargs)

        if can_edit_work_type:
            self.fields['work_type'] = forms.ChoiceField(choices=Order.WORK_TYPE_CHOICES, initial=order.work_type)
        if can_edit_note:
            self.fields['note'] = forms.CharField(widget=forms.Textarea, initial=order.note)
        if can_edit_status:
            self.fields['status'] = forms.ChoiceField(choices=Order.STATUS_CHOICES, initial=order.status, widget=forms.RadioSelect)
        if can_edit_vendor:
            self.fields['vendor'] = forms.ModelChoiceField(
                queryset=Vendor.objects.all(),
                empty_label="Choose a vendor",
                initial=order.vendor
            )
        if can_edit_fa_date:
            self.fields['fa_date'] = forms.DateTimeField(initial=order.fa_date, label="first appointment suggested time")
        if can_edit_fa_duration:
            self.fields['fa_duration'] = forms.IntegerField(min_value=1, initial=order.fa_duration, label="first appointment duration")
        if can_accept_fa:
            if user.profile.has_user_types(['te', 'mo', 'ad']):
                self.fields['fa_status_creator'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.fa_status_creator, widget=forms.RadioSelect, label="accept first appointment time?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['fa_status_creator'].label += ' (creator)'
            if user.profile.has_user_types(['ve', 'vm', 'mo', 'ad']):
                self.fields['fa_status_vendor'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.fa_status_vendor, widget=forms.RadioSelect, label="accept first appointment time?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['fa_status_vendor'].label += ' (vendor)'
        if can_edit_quote:
            self.fields['quote'] = forms.DecimalField(initial=order.quote)
        if can_accept_quote:
            if user.profile.has_user_types(['pm', 'mo', 'ad']):
                self.fields['quote_status_approver'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.quote_status_approver, widget=forms.RadioSelect, label="accept quote?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['quote_status_approver'].label += ' (approver)'
            if user.profile.has_user_types(['po', 'mo', 'ad']):
                self.fields['quote_status_owner'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.quote_status_owner, widget=forms.RadioSelect, label="accept quote?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['quote_status_owner'].label += ' (owner)'
        if can_edit_sa_date:
            self.fields['sa_date'] = forms.DateTimeField(initial=order.sa_date, label="second appointment suggested time")
        if can_edit_sa_duration:
            self.fields['sa_duration'] = forms.IntegerField(min_value=1, initial=order.sa_duration, label="second appointment duration")
        if can_accept_sa:
            if user.profile.has_user_types(['te', 'mo', 'ad']):
                self.fields['sa_status_creator'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.sa_status_creator, widget=forms.RadioSelect, label="accept second appointment time?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['sa_status_creator'].label += ' (creator)'
            if user.profile.has_user_types(['ve', 'vm', 'mo', 'ad']):
                self.fields['sa_status_vendor'] = forms.ChoiceField(choices=Order.ACCEPT_CHOICES, initial=order.sa_status_vendor, widget=forms.RadioSelect, label="accept second appointment time?")
                if user.profile.has_user_types(['mo', 'ad']):
                    self.fields['sa_status_vendor'].label += ' (vendor)'
        if can_edit_payment:
            self.fields['payment'] = forms.DecimalField(initial=order.payment)

    def clean(self):
        super(OrderDetailForm, self).clean()

        if 'note' in self.cleaned_data:
            if len(self.cleaned_data['note']) < 50:
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
