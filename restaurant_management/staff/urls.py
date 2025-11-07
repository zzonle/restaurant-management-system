from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    # Employee URLs
    path('', employee_list, name='employee_list'),
    path('create/', employee_create, name='employee_create'),
    path('<int:pk>/', employee_detail, name='employee_detail'),
    path('<int:pk>/edit/', employee_edit, name='employee_edit'),
    path('<int:pk>/delete/', employee_delete, name='employee_delete'),
]
