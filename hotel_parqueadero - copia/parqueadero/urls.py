from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('crear_parqueadero/', views.crear_parqueadero, name='crear_parqueadero'),
    path('listar_vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('buscar_eliminar_vehiculo/', views.buscar_eliminar_vehiculo, name='buscar_eliminar_vehiculo'),
    path('ver_disponibilidad/', views.ver_disponibilidad, name='ver_disponibilidad'),
    path('ingresar_vehiculo/', views.ingresar_vehiculo, name='ingresar_vehiculo'),
    path('eliminar_vehiculos/', views.eliminar_vehiculos, name='eliminar_vehiculos'),
    path('editar_eliminar_parqueadero/<int:parqueadero_id>/', views.editar_eliminar_parqueadero, name='editar_eliminar_parqueadero'),
    path('eliminar_parqueadero/<int:parqueadero_id>/', views.eliminar_parqueadero, name='eliminar_parqueadero'),
    path('listar_parqueaderos/', views.listar_parqueaderos, name='listar_parqueaderos'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

]
