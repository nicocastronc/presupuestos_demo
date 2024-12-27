from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Presupuesto(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADO', 'Enviado'),
        ('ACEPTADO', 'Aceptado'),
        ('RECHAZADO', 'Rechazado')
    ]

    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_validez = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    notas = models.TextField(blank=True)

    @property
    def total(self):
        return sum(item.precio_total for item in self.items.all())

class ItemPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, related_name='items', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)