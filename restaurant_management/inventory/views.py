from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages
from .models import InventoryItem

# Form integrated in views
class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'unit', 'reorder_level', 'category']

# Inventory CRUD Views
def inventory_list(request):
    items = InventoryItem.objects.all().order_by('category', 'name')
    return render(request, 'inventory/inventory_list.html', {'items': items})

def inventory_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item añadido correctamente')
            return redirect('inventory_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item actualizado correctamente')
            return redirect('inventory_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, 'Item eliminado correctamente')
            return redirect('inventory_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el item: {str(e)}')
    return render(request, 'inventory/inventory_confirm_delete.html', {'item': item})

def check_stock(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if item.quantity <= item.reorder_level:
        messages.warning(request, f'Stock bajo para {item.name}. Considere reordenar.')
    return render(request, 'inventory/inventory_detail.html', {'item': item})
