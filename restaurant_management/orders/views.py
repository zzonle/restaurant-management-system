from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Order, OrderItem
from menu.models import MenuItem

# Forms
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'status']

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
