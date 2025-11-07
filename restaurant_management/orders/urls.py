from django.urls import path
from .views import (
    order_list, order_detail, order_create, order_update, order_delete,
    item_create, item_update, item_delete
)

app_name = "orders"

urlpatterns = [
    path("", order_list, name="order_list"),
    path("nuevo/", order_create, name="order_create"),
    path("<int:pk>/", order_detail, name="order_detail"),
    path("<int:pk>/editar/", order_update, name="order_update"),
    path("<int:pk>/eliminar/", order_delete, name="order_delete"),

    path("<int:order_pk>/items/nuevo/", item_create, name="item_create"),
    path("items/<int:pk>/editar/", item_update, name="item_update"),
    path("items/<int:pk>/eliminar/", item_delete, name="item_delete"),
]
