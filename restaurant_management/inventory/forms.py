from django import forms
from .models import Inventory, Supplier

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'quantity', 'supplier', 'last_ordered']
        widgets = {'last_ordered': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'phone', 'email']
