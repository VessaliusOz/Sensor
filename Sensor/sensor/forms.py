from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, label=u'用户名')
    password = forms.CharField(widget=forms.PasswordInput, label=u'密码')