from django.urls import path
from .views import views
#inventory
from .views.inventory import products, categories, suppliers
#rrhh
from .views.rrhh import Employees, EmployeeTerritories, Region, Territories
from .views.rrhh.Employees import EmployeeListCreateView, EmployeeDetailView
#ventas
from .views.ventas import Customers, Order_Details, Orders, Shippers

urlpatterns = [
    path('inventario/',  views.inventario),
    path('rrhh/', views.rrhh),
    path('ventas/', views.ventas),
    #---------------------inventory-----------------------------------
    #productos
    path('productos/', products.productsListCreateView.as_view()),
    path('productos/<int:id_producto>/', products.productsDetailView.as_view()),
    
    #categorias
    path('categorias/', categories.CategoriesListCreateView.as_view()),
    path('categorias/<int:id_categoria>/', categories.CategoriesDetailsView.as_view()),

    #suppliers
    path('suppliers/buscar/', suppliers.suppliersListCreateView.as_view()),
    path('suppliers/borrar/<int:id_suppler>/', suppliers.suppliersDetailView.as_view()),
    #---------------------inventory-----------------------------------

    #---------------------rrhh-----------------------------------
    #employees
    path('employees/', Employees.EmployeeListCreateView.as_view(), name='empleados-lista-crear'),
    path('employees/<int:id_empleado>/', Employees.EmployeeDetailView.as_view()),
    # --- Regiones ---
    path('region/', Region.RegionListCreateView.as_view(), name='region-list-create'),
    path('region/<int:id_region>/', Region.RegionDetailView.as_view(), name='region-detail'),

    # --- Territorios ---
    path('territories/', Territories.TerritoryListCreateView.as_view(), name='territory-list-create'),
    path('territories/<str:id_territorio>/', Territories.TerritoryDetailView.as_view(), name='territory-detail'),

    # --- EmployeeTerritories (Relación Empleado-Territorio) ---
    path('employee-territories/', EmployeeTerritories.EmployeeTerritoriesCreateView.as_view(), name='employee-territories-list'),
    path('employee-territories/<int:id_EmployeeTerritory>/', EmployeeTerritories.EmployeeTerritoriesDetailView.as_view(), name='employee-territories-detail'),
    #---------------------rrhh-----------------------------------

    #---------------------ventas-----------------------------------
    #Customers
    path('customers/', Customers.CustomerListCreateView.as_view()),
    path('customers/<int:id_cliente>/', Customers.CustomerDetailView.as_view()),

    #Order_details
    path('order_details/', Order_Details.OrderDetailListCreateView.as_view()),
    path('order_details/<int:id_orden>/<int:id_producto>/ ', Order_Details.OrderDetailDetailView.as_view()),

    #Orders
    path('orders/', Orders.OrderListCreateView.as_view()),
    path('orders/<int:id_order>', Orders.OrderDetailView.as_view()),

    #Shippers
    path('shippers/', Shippers.ShipperListCreateView.as_view()),
    path('shippers/<int:id_shipper>', Shippers.ShipperDetailView.as_view()),
    #---------------------ventas-----------------------------------

    ]