﻿from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from AuctionApp.models import Item, TaskStatus, Task, Message

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

# unused
class BootstrapUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password again'}))
    first_name = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'First name'}))
    last_name = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Last name'}))
    email = forms.EmailField(max_length=100,
                               widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(User, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserInfoEditForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'User name',
                                   'readonly':'readonly'}))
    first_name = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'First name'}))
    last_name = forms.CharField(max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Last name'}))
    email = forms.EmailField(max_length=100,
                               widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CreateItemForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, 
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Name'}))
    price = forms.FloatField(required=True,
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Price'}))
    class Meta:
        model = Item
        fields = ['name', 'price',]

class EditItemForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, 
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Name'}))
    price = forms.FloatField(required=True,
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Price'}))
    class Meta:
        model = Item
        fields = ['name', 'price',]

class CreateTaskStatusForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, 
                            widget=forms.TextInput({
                                'class': 'form-control',
                                'placeholder':'Status name'}))
    class Meta:
        model = TaskStatus
        fields = ['name',]

class CreateTaskForm(forms.ModelForm):
    text = forms.CharField(max_length=500, required=True, 
                            widget=forms.Textarea({
                                'class': 'form-control',
                                'placeholder':'Text',
                                'rows':'3'}))
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all(), empty_label='Select status', initial=0,
                        widget=forms.Select({
                            'class': 'form-control',}))

    class Meta:
        model = Task
        fields = ['text', 'status']

class EditTaskForm(forms.ModelForm):
    text = forms.CharField(max_length=500, required=True, 
                            widget=forms.Textarea({
                                'class': 'form-control',
                                'placeholder':'Text',
                                'rows':'3'}))
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all(), empty_label='Select status', initial=0,
                        widget=forms.Select({
                            'class': 'form-control',}))
    deleted = forms.BooleanField(required=False)

    class Meta:
        model = Task
        fields = ['text', 'status', 'deleted']

class SendMessageForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput({
                                'class': 'form-control',
                                'placeholder':'User name',
                                'readonly':'readonly'}))
    text = forms.CharField(required=True,
                        widget=forms.Textarea({
                            'class': 'form-control',
                            'placeholder':'Message text',
                            'rows':'10'}))
    class Meta:
        model = Message
        fields = ['username', 'text']