from django.urls import path
from .views import item_list, item_create, item_update, item_delete

app_name = "menu"

urlpatterns = [
    path("", item_list, name="list"),
    path("nuevo/", item_create, name="create"),
    path("<int:pk>/editar/", item_update, name="update"),
    path("<int:pk>/eliminar/", item_delete, name="delete"),
]
