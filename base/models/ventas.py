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
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer_id', blank=True, null=True)
    # Recomendación: Si tienes el modelo Employee, cámbialo a ForeignKey('base.Employee', ...)
    employee_id = models.IntegerField(db_column='employee_id', blank=True, null=True) 
    order_date = models.DateField(db_column='order_date', blank=True, null=True)
    required_date = models.DateField(db_column='required_date', blank=True, null=True)
    shipped_date = models.DateField(db_column='shipped_date', blank=True, null=True)
    ship_via = models.ForeignKey(Shipper, models.DO_NOTHING, db_column='ship_via', blank=True, null=True)
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
        return f"Orden {self.id}"

class OrderDetail(models.Model):
    # SOLUCIÓN AL WARNING: Eliminamos primary_key=True del ForeignKey
    order = models.ForeignKey(Order, models.DO_NOTHING, db_column='order_id')
    product = models.ForeignKey('base.Producto', models.DO_NOTHING, db_column='product_id')
    unit_price = models.DecimalField(db_column='unit_price', max_digits=10, decimal_places=2)
    quantity = models.SmallIntegerField(db_column='quantity')
    discount = models.FloatField(db_column='discount')

    class Meta:
        managed = False
        db_table = 'order_details'
        # IMPORTANTE: Como Northwind usa llave compuesta, Django necesita un truco.
        # Al no tener un ID único, le decimos que la combinación de ambos es única.
        unique_together = (('order', 'product'),)

    # TRUCO FINAL: Para que Django no llore por la falta de una Primary Key real en un modelo 'managed=False'
    # a veces es necesario definir un ID ficticio si vas a usar el Admin de Django.
    # Pero para tu API, con unique_together debería bastar.

    def __str__(self):
        return f"Detalle {self.order_id} - {self.product_id}"