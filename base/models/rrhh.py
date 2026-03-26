from django.db import models

class Region(models.Model):
    id = models.IntegerField(db_column='region_id', primary_key=True)
    description = models.CharField(db_column='region_description', max_length=50)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.description.strip()

class Territory(models.Model):
    id = models.CharField(db_column='territory_id', primary_key=True, max_length=20)
    description = models.CharField(db_column='territory_description', max_length=50)
    region = models.ForeignKey('Region',  
                               db_column='region_id',
                               null=True,
                               on_delete=models.DO_NOTHING,
                               related_name='region_employee'
                               )

    class Meta:
        managed = False
        db_table = 'territories'

    def __str__(self):
        return self.description.strip()

class Employee(models.Model):
    id = models.AutoField(db_column='employee_id', primary_key=True)
    last_name = models.CharField(db_column='last_name', max_length=20)
    first_name = models.CharField(db_column='first_name', max_length=10)
    title = models.CharField(db_column='title', max_length=30, blank=True, null=True)
    title_of_courtesy = models.CharField(db_column='title_of_courtesy', max_length=25, blank=True, null=True)
    birth_date = models.DateField(db_column='birth_date', blank=True, null=True)
    hire_date = models.DateField(db_column='hire_date', blank=True, null=True)
    address = models.CharField(db_column='address', max_length=60, blank=True, null=True)
    city = models.CharField(db_column='city', max_length=15, blank=True, null=True)
    region = models.CharField(db_column='region', max_length=15, blank=True, null=True)
    postal_code = models.CharField(db_column='postal_code', max_length=10, blank=True, null=True)
    country = models.CharField(db_column='country', max_length=15, blank=True, null=True)
    home_phone = models.CharField(db_column='home_phone', max_length=24, blank=True, null=True)
    extension = models.CharField(db_column='extension', max_length=4, blank=True, null=True)
    photo = models.BinaryField(db_column='photo', blank=True, null=True)
    notes = models.TextField(db_column='notes', blank=True, null=True)
    # Relación recursiva: un empleado reporta a otro empleado
    reports_to = models.ForeignKey(
            'self',
            models.DO_NOTHING,
            db_column='reports_to',
            blank=True,
            null=True,
            related_name='subordinados'  # ← así podés hacer empleado.subordinados.all()
        )
    photo_path = models.CharField(db_column='photo_path', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployeeTerritory(models.Model):
    # Esta es una tabla intermedia para la relación Many-to-Many entre Empleados y Territorios
    employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='employee_id')
    territory = models.ForeignKey('Territory',
                                  db_column='territory_id',
                                  null= True, 
                                  on_delete=models.DO_NOTHING,
                                  related_name= 'territory_employee'
                                  )

    class Meta:
        managed = False
        db_table = 'employee_territories'
        unique_together = (('employee', 'territory'),)

    def __str__(self):
        return f"{self.employee} -> {self.territory}"