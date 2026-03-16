#centro de configuración de la base de datos
from django.db import models

# Create your models here.

# Class product table
#--------------------------------------------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------------


#Class categories table
#--------------------------------------------------------------------------------------------------
class categories(models.Model):
    # Mapa completo de la tabla 'products' de Northwind
    id = models.AutoField(primary_key=True, db_column='category_id')
    nombre = models.CharField(max_length=40, db_column='category_name')
    descripcion = models.TextField(db_column='description')

    class Meta:
        managed = False
        db_table = 'categories'

#--------------------------------------------------------------------------------------------------

#Class suppliers table
#--------------------------------------------------------------------------------------------------
class Supplier(models.Model):
    # Usamos db_column para apuntar exactamente al nombre en la base de datos
    id = models.AutoField(db_column='supplier_id', primary_key=True) 
    company_name = models.CharField(db_column='company_name', max_length=40)
    contact_name = models.CharField(db_column='contact_name', max_length=30, blank=True, null=True)
    contact_title = models.CharField(db_column='contact_title', max_length=30, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=60, blank=True, null=True)
    city = models.CharField(db_column='city', max_length=15, blank=True, null=True)
    region = models.CharField(db_column='region', max_length=15, blank=True, null=True)
    postal_code = models.CharField(db_column='postal_code', max_length=10, blank=True, null=True)
    country = models.CharField(db_column='country', max_length=15, blank=True, null=True)
    phone = models.CharField(db_column='phone', max_length=24, blank=True, null=True)
    fax = models.CharField(db_column='fax', max_length=24, blank=True, null=True)
    homepage = models.TextField(db_column='homepage', blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'suppliers' 

    def __str__(self):
        return self.company_name
#--------------------------------------------------------------------------------------------------