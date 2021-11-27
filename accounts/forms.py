from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Enter Password',
    #     'class': 'form-control',
    # }))
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Confirm Password'
    # }))

    class Meta:
        model = Account
        fields = ['full_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        print(password)
        # confirm_password = cleaned_data.get('password2')

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password does not match!"
    #         )

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields['full_name'].widget.attrs['placeholder'] = 'Enter Full Name'
    #     # self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
    #     self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'
