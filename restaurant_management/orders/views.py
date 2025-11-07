from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Order, OrderItem
from menu.models import MenuItem
from customers.models import Customer


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
        fields = ['customer_name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el pedido ya tiene texto en customer_name, intenta preseleccionar el cliente
        if self.instance and self.instance.pk and self.instance.customer_name:
            try:
                cliente = Customer.objects.get(name=self.instance.customer_name)
                self.fields['customer_name'].initial = cliente.pk
            except Customer.DoesNotExist:
                self.fields['customer_name'].help_text = (
                    f'El cliente "{self.instance.customer_name}" no existe. '
                    'Selecciona uno de la lista.'
                )

    def clean_customer_name(self):
        # Guardamos solo el nombre del cliente como texto (porque Order tiene un CharField)
        cliente = self.cleaned_data['customer_name']
        return cliente.name
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price']

# Order Views
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.orderitem_set.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:order_detail', pk=pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

# OrderItem Views
def item_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            order.calculate_total()
            return redirect('orders:order_detail', pk=order_pk)
    else:
        form = OrderItemForm()
    return render(request, 'orders/orderitem_form.html', {'form': form, 'order': order})

def item_update(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            item.order.calculate_total()
            return redirect('orders:order_detail', pk=item.order.pk)
    else:
        form = OrderItemForm(instance=item)
    return render(request, 'orders/orderitem_form.html', {'form': form, 'item': item})

def item_delete(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    order_pk = item.order.pk
    if request.method == 'POST':
        item.delete()
        item.order.calculate_total()
        return redirect('orders:order_detail', pk=order_pk)
    return render(request, 'orders/orderitem_confirm_delete.html', {'item': item})
