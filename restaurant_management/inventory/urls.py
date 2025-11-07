from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("nuevo/", views.inventory_create, name="inventory_create"),
    path("<int:pk>/editar/", views.inventory_edit, name="inventory_edit"),
    path("<int:pk>/eliminar/", views.inventory_delete, name="inventory_delete"),
    path("<int:pk>/check/", views.check_stock, name="inventory_check"),
]
