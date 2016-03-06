from django import forms

class ParkSearchForm(forms.Form):
    park_name = forms.CharField(label='Park Name', max_length=200)