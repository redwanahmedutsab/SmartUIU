from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_image', 'email', 'mobile', 'item_name', 'location', 'time_date', 'description']
