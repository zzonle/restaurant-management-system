
from django import forms
from customers.models import Customer
from .models import Order

class OrderForm(forms.ModelForm):
    customer_name = forms.ModelChoiceField(
        queryset=Customer.objects.order_by('name'),
        label='Cliente',
        empty_label='— Selecciona un cliente —',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-all duration-200 bg-gray-50'
        })
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'status', 'order_date', 'total', 'notes']

    def clean_customer_name(self):
        customer = self.cleaned_data['customer_name']
        return customer.name  # guarda el texto en el CharField
