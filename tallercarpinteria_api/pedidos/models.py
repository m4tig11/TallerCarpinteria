from django.db import models

class Pedido(models.Model):
    cliente_nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    fecha_medicion = models.DateField()
    presupuesto = models.FloatField()
    fecha_llegada_materiales = models.DateField()
    fecha_entrega = models.DateField()
    ruta_plano = models.CharField(max_length=255)
    notas = models.TextField()

    def __str__(self):
        return self.cliente_nombre
