from django import forms

class ParkSearchForm(forms.Form):
    park_name = forms.CharField(label='Find A Park', max_length=200)
