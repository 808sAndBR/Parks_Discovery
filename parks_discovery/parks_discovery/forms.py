from django import forms

class ParkSearchForm(forms.Form):
    park_name = forms.CharField(label='Your Favorite Park', max_length=200)
