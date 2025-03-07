from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    cliente_nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=50)
    fecha_medicion = models.DateField()
    presupuesto = models.FloatField()
    fecha_llegada_materiales = models.DateField()
    fecha_entrega = models.DateField()
    plano = models.ImageField(upload_to='planos/', null=True, blank=True)
    notas = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cliente_nombre
