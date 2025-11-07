# ...existing code...
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Employee

# Form integrado en la view
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'salary']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres')
        return name

    def clean_position(self):
        position = self.cleaned_data.get('position', '').strip()
        if not position:
            raise ValidationError('La posición es requerida')
        return position

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is None or salary <= 0:
            raise ValidationError('El salario debe ser mayor que 0')
        return salary

# CRUD Views para Employee
def employee_list(request):
    employees = Employee.objects.all().order_by('name')
    return render(request, 'staff/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'staff/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Empleado creado correctamente')
                    return redirect('staff:employee_list')
            except Exception as e:
                messages.error(request, f'Error al crear empleado: {e}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario')
    else:
        form = EmployeeForm()
    return render(request, 'staff/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Empleado actualizado correctamente')
                    return redirect('staff:employee_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar empleado: {e}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'staff/employee_form.html', {'form': form, 'employee': employee})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            employee.delete()
            messages.success(request, 'Empleado eliminado correctamente')
            return redirect('staff:employee_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar empleado: {e}')
    return render(request, 'staff/employee_confirm_delete.html', {'employee': employee})
# ...existing code...
