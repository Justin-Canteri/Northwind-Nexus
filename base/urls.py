from django.urls import path
from .views import views, register
#inventory
from .views.inventory import products, categories, suppliers
#rrhh
from .views.rrhh import Employees, EmployeeTerritories, Region, Territories
from .views.rrhh.Employees import EmployeeListCreateView, EmployeeDetailView
#ventas
from .views.ventas import Customers, Order_Details, Orders, Shippers

urlpatterns = [
    path('', views.inicio),

    path('api/register/', register.registrar_usuario),
    #---------------------inventory-----------------------------------
    #productos
    path('productos/buscar/', products.buscar),
    path('productos/crear/', products.crear_producto),
    path('productos/borrar/<int:id_producto>/', products.delete_producto),
    path('productos/editar/<int:id_producto>/', products.editar_producto),

    #categorias
    path('categorias/buscar/', categories.buscar),
    path('categorias/crear/', categories.crear_categoria),
    path('categorias/borrar/<int:id_producto>/', categories.delete_categoria),
    path('categorias/editar/<int:id_producto>/', categories.editar_categoria),

    #suppliers
    path('suppliers/buscar/', suppliers.buscar),
    path('suppliers/crear/', suppliers.crear_supplier),
    path('suppliers/borrar/<int:id_suppler>/', suppliers.delete_supplier),
    path('suppliers/editar/<int:id_suppler>/', suppliers.editar_supplier),
    #---------------------inventory-----------------------------------

    #---------------------rrhh-----------------------------------
    #employees
    path('employees/', EmployeeListCreateView.as_view(), name='empleados-lista-crear'),
    # urls.py
    path('employees/<int:id_empleado>/', EmployeeDetailView.as_view()),
    #path('employees/buscar/', Employees.buscar_empleados),
    #path('employees/crear/', Employees.crear_empleado),
    #path('employees/borrar/<int:id_empleado>/', Employees.eliminar_empleado),
    #path('employees/editar/<int:id_empleado>/', Employees.editar_empleado),

    #EmployeeTerritories
    path('employeeTerritories/buscar/', EmployeeTerritories.buscar_asignaciones),
    path('employeeTerritories/crear/', EmployeeTerritories.asignar_territorio),
    path('employeeTerritories/borrar/<int:id_empleado>/<str:id_territorio>/', EmployeeTerritories.eliminar_asignacion),

    #Region
    path('region/buscar/', Region.buscar_regiones),
    path('region/crear/', Region.crear_region),
    path('region/borrar/<int:id_region>/', Region.eliminar_region),
    path('region/editar/<int:id_region>/', Region.editar_region),

    #Territorios
    path('terrirories/buscar/', Territories.buscar_territorios),
    path('terrirories/crear/', Territories.crear_territorio),
    path('terrirories/borrar/<int:id_territorio>/', Territories.eliminar_territorio),
    path('terrirories/editar/<int:id_territorio>/', Territories.editar_territorio),
    #---------------------rrhh-----------------------------------

    #---------------------ventas-----------------------------------
    #Customers
    path('customers/buscar/', Customers.buscar_clientes),
    path('customers/crear/', Customers.crear_cliente),
    path('customers/borrar/<int:id_cliente>/', Customers.eliminar_cliente),
    path('customers/editar/<int:id_cliente>/', Customers.editar_cliente),

    #Order_details
    path('order_details/buscar/', Order_Details.buscar_detalles),
    path('order_details/crear/', Order_Details.crear_detalle),
    path('order_details/borrar/<int:id_orden>/<int:id_producto>/ ', Order_Details.eliminar_detalle),
    path('order_details/editar/<int:id_orden>/<int:id_producto>/', Order_Details.editar_detalle),

    #Orders
    path('orders/buscar/', Orders.buscar),
    path('orders/crear/', Orders.crear_order),
    path('orders/borrar/<int:id_order>', Orders.eliminar_order),
    path('orders/editar/<int:id_order>', Orders.editar_order),

    #Shippers
    path('shippers/buscar/', Shippers.buscar_shippers),
    path('shippers/crear/', Shippers.crear_shipper),
    path('shippers/borrar/<int:id_shipper>', Shippers.eliminar_shipper),
    path('shippers/editar/<int:id_shipper>', Shippers.editar_shipper),
    #---------------------ventas-----------------------------------

    ]