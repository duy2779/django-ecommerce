from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from store.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Nhập lại mật khẩu'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
        "username": "Tên tài khoản"
    }
        widgets ={
            'username':forms.TextInput(attrs={'class':'input100', 'placeholder':'Tên tài khoản'}),
            'email':forms.TextInput(attrs={'class':'input100', 'placeholder':'Email'})
        }
        error_messages = {
            'username': {
                'unique': "Tên tài khoản đã tồn tại",
            },
        }

    def __init__(self, *args, **kwargs):
        self.error_messages['password_mismatch'] = 'Mật khẩu nhập lại không khớp'
        super().__init__(*args, **kwargs)
