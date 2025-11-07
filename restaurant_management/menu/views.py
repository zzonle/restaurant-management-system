from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']  

def item_list(request):
    """Listar (READ)"""
    items = MenuItem.objects.all()
    return render(request, 'menu/menu_list.html', {'items': items})

def item_create(request):
    """Crear (CREATE)"""
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu:list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/menu_form.html', {'form': form})

def item_update(request, pk):
    """Actualizar (UPDATE)"""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu:list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/menu_form.html', {'form': form, 'item': item})

def item_delete(request, pk):
    """Eliminar (DELETE)"""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu:list')
    return render(request, 'menu/menu_confirm_delete.html', {'item': item})
