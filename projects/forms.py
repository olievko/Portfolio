from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    contact_name = forms.CharField(
        label=_('Contact name'),
        max_length=100,
        widget=forms.TextInput(attrs={'size': '39', 'class': 'form-control'}))
    contact_email = forms.EmailField(
        label=_('Contact email'),
        widget=forms.TextInput(attrs={'size': '39', 'class': 'form-control'}))
    subject = forms.CharField(
        label=_('Subject'),
        max_length=100,
        widget=forms.TextInput(attrs={'size': '39', 'class': 'form-control'}))
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    cc_myself = forms.BooleanField(
        label=_('Send copy to myself'),
        required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', )
