# customers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Customers
    path("", views.customer_list, name="customer_list"),
    path("nuevo/", views.customer_create, name="customer_create"),
    path("<int:pk>/editar/", views.customer_edit, name="customer_edit"),
    path("<int:pk>/eliminar/", views.customer_delete, name="customer_delete"),
    path("<int:pk>/", views.customer_detail, name="customer_detail"),

    # Reservations
    path("reservas/", views.reservation_list, name="reservation_list"),
    path("<int:customer_pk>/reservas/nueva/", views.reservation_create, name="reservation_create"),
    path("reservas/<int:pk>/editar/", views.reservation_edit, name="reservation_edit"),
    path("reservas/<int:pk>/eliminar/", views.reservation_delete, name="reservation_delete"),
]
