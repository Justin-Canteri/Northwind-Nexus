#centro de configuración de la base de datos
from django.db import models

# Create your models here.


class Producto(models.Model):
    # Mapa completo de la tabla 'products' de Northwind
    id = models.AutoField(primary_key=True, db_column='product_id')
    nombre = models.CharField(max_length=40, db_column='product_name')
    proveedor_id = models.IntegerField(db_column='supplier_id', null=True)
    categoria_id = models.IntegerField(db_column='category_id', null=True)
    cantidad_por_unidad = models.CharField(max_length=20, db_column='quantity_per_unit', null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, db_column='unit_price')
    stock = models.SmallIntegerField(db_column='units_in_stock')
    descontinuado = models.IntegerField(db_column='discontinued') # 0 o 1

    class Meta:
        managed = False
        db_table = 'products'
