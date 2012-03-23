from django import forms

class AddComment( forms.Form ) :
    comment = forms.CharField( widget = forms.Textarea, min_length = 5, max_length = 500 )
