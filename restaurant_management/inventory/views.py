# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inventory, Supplier
from .forms import InventoryForm, SupplierForm

# Inventory CRUD Views
def inventory_list(request):
    # Ajusta el orden según campos reales del modelo
    # Si no tienes 'category', puedes quitarlo o dejar solo item_name
    items = Inventory.objects.all().order_by('item_name')
    return render(request, 'inventory/inventory_list.html', {'items': items})

def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem añadido correctamente')
            return redirect('inventory_list')  # o 'inventory:inventory_list' si usas namespace
        messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem actualizado correctamente')
            return redirect('inventory_list')
        messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, 'Ítem eliminado correctamente')
            return redirect('inventory_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el ítem: {str(e)}')
    return render(request, 'inventory/inventory_confirm_delete.html', {'item': item})

def check_stock(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    reorder_level = getattr(item, 'reorder_level', 0)  # por si tu modelo lo tiene
    if item.quantity <= reorder_level:
        messages.warning(request, f'Stock bajo para {getattr(item, "item_name", "ítem")}. Considera reordenar.')
    return render(request, 'inventory/inventory_detail.html', {'item': item})
