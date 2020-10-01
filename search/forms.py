
from django import forms


class inputForm(forms.Form):
    query = forms.CharField(label='', max_length=264, widget=forms.TextInput(attrs={
        'placeholder': 'Search Here........',
        'style': 'border: 2px solid red; border-radius: 25px;',
    }))
