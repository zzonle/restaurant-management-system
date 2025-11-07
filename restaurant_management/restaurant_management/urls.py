from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customers/", include("customers.urls")),
    path("menu/", include("menu.urls")),
    path("orders/", include("orders.urls")),
    path("inventory/", include("inventory.urls")),
    path("staff/", include("staff.urls")),
    path("", include("menu.urls")),  
]
