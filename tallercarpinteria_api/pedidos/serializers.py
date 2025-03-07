

from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')  # Solo lectura para evitar cambios manuales
    plano = serializers.FileField(required=False)  # Ahora acepta archivos

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_plano(self, obj):
        if obj.plano:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.plano.url)
        return None