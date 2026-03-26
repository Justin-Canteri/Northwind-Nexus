from rest_framework import serializers
from .models import rrhh, inventory, ventas # Ajusta la ruta a tu modelo

#modelos rrhh
'''----------------------------------------------------------------------------'''
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = rrhh.Region
        # Aquí eliges qué campos quieres que "viajen" por la API
        fields = [
            'id', 'description'
        ]
        # O puedes usar '__all__' para incluirlos todos

class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = rrhh.Territory
        # Aquí eliges qué campos quieres que "viajen" por la API
        fields = [
            'id', 'description', 'region'
        ]
        # O puedes usar '__all__' para incluirlos todos


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = rrhh.Employee
        # Aquí eliges qué campos quieres que "viajen" por la API
        fields = [
            'id', 'first_name', 'last_name', 'title', 
            'birth_date', 'hire_date', 'city', 'country', 'reports_to'
        ]
        # O puedes usar '__all__' para incluirlos todos
class EmployeeTerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = rrhh.EmployeeTerritory
        # Aquí eliges qué campos quieres que "viajen" por la API
        fields = [
            'employee', 'territory'
        ]
        # O puedes usar '__all__' para incluirlos todos
'''----------------------------------------------------------------------------'''

#modelos inventory
'''----------------------------------------------------------------------------'''

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventory.Supplier
        fields = '__all__'
        
class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = inventory.categories

        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = categoriesSerializer(read_only=True)
    proveedor = SupplierSerializer(read_only = True)
    class Meta:
        model = inventory.Producto
        fields = '__all__'
'''----------------------------------------------------------------------------'''

#modelos ventas
'''----------------------------------------------------------------------------'''
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ventas.Customer
        fields = [
            '__all__'
        ]
class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ventas.Shipper
        fields = [
            '__all__'
        ]
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ventas.Order
        fields = [
            '__all__'
        ]
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ventas.OrderDetail
        fields = [
            '__all__'
        ]
'''----------------------------------------------------------------------------'''