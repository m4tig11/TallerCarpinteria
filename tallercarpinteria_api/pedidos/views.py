from django.shortcuts import render
from rest_framework import viewsets
from .models import Pedido
from .serializers import PedidoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    


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