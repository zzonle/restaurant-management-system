# orders/forms.py (o donde tengas OrderItemForm)
from django import forms
from .models import OrderItem
from menu.models import MenuItem

class OrderItemForm(forms.ModelForm):
    # 🔒 lo hacemos opcional en el form + escondido
    price = forms.DecimalField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price']
        widgets = {
            'item': forms.Select(attrs='class:w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-all duration-200 bg-gray-50'),
            'quantity': forms.NumberInput(attrs={'min':1,'class':'w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-all duration-200 bg-gray-50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = MenuItem.objects.order_by('name')
        self.fields['item'].label_from_instance = lambda o: f"{o.name} — ${o.price}"

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get('item')
        price = cleaned.get('price')
        # ✅ si por cualquier motivo no vino price, lo tomamos del ítem
        if item and (price is None or price == ''):
            cleaned['price'] = item.price
        return cleaned
