from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Customer, Reservation

# Forms integrated in views
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'number_of_people']

# Customer CRUD Views
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'customers/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

# Reservation CRUD Views
def reservation_list(request):
    reservations = Reservation.objects.all().order_by('-reservation_date')
    return render(request, 'customers/reservation_list.html', {'reservations': reservations})

def reservation_create(request, customer_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = customer
            reservation.save()
            return redirect('customer_detail', pk=customer_pk)
    else:
        form = ReservationForm()
    return render(request, 'customers/reservation_form.html', 
                 {'form': form, 'customer': customer})

def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=reservation.customer.pk)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'customers/reservation_form.html', {'form': form})

def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    customer_pk = reservation.customer.pk
    if request.method == 'POST':
        reservation.delete()
        return redirect('customer_detail', pk=customer_pk)
    return render(request, 'customers/reservation_confirm_delete.html', 
                 {'reservation': reservation})
