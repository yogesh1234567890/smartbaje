from django import forms
from .models import CustomerQuery


class CustomerQueryForm(forms.ModelForm):
    class Meta:
        model = CustomerQuery
        fields = '__all__'