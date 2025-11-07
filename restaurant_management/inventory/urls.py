from django.urls import path
from . import views

urlpatterns = [
    path("", inventory_list, name="inventory_list"),
    path("nuevo/", inventory_create, name="inventory_create"),
    path("<int:pk>/editar/", inventory_edit, name="inventory_edit"),
    path("<int:pk>/eliminar/", inventory_delete, name="inventory_delete"),
    path("<int:pk>/check/", check_stock, name="inventory_check"),
]
