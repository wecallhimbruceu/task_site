from .models import Message, User
from django.forms import ModelForm
from django.forms import PasswordInput


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {'password': PasswordInput()}


class SendMessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ('email', 'message')
