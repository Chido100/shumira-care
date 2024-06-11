from django import forms
from .models import Item


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image']