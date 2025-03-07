from django.shortcuts import render
from rest_framework import viewsets
from .models import Pedido
from .serializers import PedidoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import Pedido
from .serializers import PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden usar la API

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)  # Solo muestra los pedidos del usuario autenticado

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)  # Guarda el usuario que crea el pedido



class PedidoPlanoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
            if 'plano' in request.FILES:
                pedido.plano = request.FILES['plano']
                pedido.save()
                return Response({'status': 'success'})
            return Response({'error': 'No file provided'}, status=400)
        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido not found'}, status=404)