

from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')  # Solo lectura para evitar cambios manuales

    class Meta:
        model = Pedido
        fields = '__all__'
