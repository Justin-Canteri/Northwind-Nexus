from django.db import models

class Customer(models.Model):
    id = models.CharField(db_column='customer_id', primary_key=True, max_length=5)
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

    class Meta:
        managed = False
        db_table = 'customers'

    def __str__(self):
        return self.company_name

class Shipper(models.Model):
    id = models.AutoField(db_column='shipper_id', primary_key=True)
    company_name = models.CharField(db_column='company_name', max_length=40)
    phone = models.CharField(db_column='phone', max_length=24, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shippers'

    def __str__(self):
        return self.company_name

class Order(models.Model):
    id = models.AutoField(db_column='order_id', primary_key=True)
    # Relación con Cliente
    customer = models.ForeignKey(Customer, 
                                 models.DO_NOTHING, 
                                 db_column='customer_id', 
                                 blank=True, 
                                 null=True, 
                                 related_name='orders')
    # Relación con Empleado (RRHH)
    employee = models.ForeignKey('Employee', 
                                 models.DO_NOTHING, 
                                 db_column='employee_id', 
                                 blank=True, null=True, 
                                 related_name='orders_sold') 
    order_date = models.DateField(db_column='order_date', blank=True, null=True)
    required_date = models.DateField(db_column='required_date', blank=True, null=True)
    shipped_date = models.DateField(db_column='shipped_date', blank=True, null=True)
    # Relación con Transportista
    ship_via = models.ForeignKey(Shipper, models.DO_NOTHING, db_column='ship_via', blank=True, null=True, related_name='shipments')
    freight = models.DecimalField(db_column='freight', max_digits=10, decimal_places=2, blank=True, null=True)
    ship_name = models.CharField(db_column='ship_name', max_length=40, blank=True, null=True)
    ship_address = models.CharField(db_column='ship_address', max_length=60, blank=True, null=True)
    ship_city = models.CharField(db_column='ship_city', max_length=15, blank=True, null=True)
    ship_region = models.CharField(db_column='ship_region', max_length=15, blank=True, null=True)
    ship_postal_code = models.CharField(db_column='ship_postal_code', max_length=10, blank=True, null=True)
    ship_country = models.CharField(db_column='ship_country', max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"Orden {self.id} - {self.customer}"

class OrderDetail(models.Model):
    # En Northwind, order_details no tiene ID propio, se usa order_id + product_id
    # Para Django, definimos uno como primary_key=True aunque sea compuesta en DB
    order = models.ForeignKey(Order, models.DO_NOTHING, db_column='order_id', primary_key=True, related_name='details')
    product = models.ForeignKey('base.Producto', models.DO_NOTHING, db_column='product_id', related_name='order_entries')
    unit_price = models.DecimalField(db_column='unit_price', max_digits=10, decimal_places=2)
    quantity = models.SmallIntegerField(db_column='quantity')
    discount = models.FloatField(db_column='discount')

    class Meta:
        managed = False
        db_table = 'order_details'
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"Detalle Orden {self.order_id} - Producto {self.product_id}"