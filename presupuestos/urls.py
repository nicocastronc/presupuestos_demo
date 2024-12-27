from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #Clientes.
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    #Servicios.
    path('servicios/', views.servicio_lista, name='servicio_lista'),
    path('servicios/nuevo/', views.servicio_crear, name='servicio_crear'),
    path('servicios/editar/<int:pk>/', views.servicio_editar, name='servicio_editar'),
    path('servicios/eliminar/<int:pk>/', views.servicio_eliminar, name='servicio_eliminar'),
    #Presupuestos.
    path('presupuestos/nuevo/', views.crear_presupuesto, name='crear_presupuesto'),
    path('presupuestos/<int:pk>/', views.detalle_presupuesto, name='detalle_presupuesto'),
    path('presupuestos/<int:pk>/pdf/', views.generar_pdf, name='generar_pdf'),
    path('get-item-form/', views.get_item_form, name='get_item_form'),
]