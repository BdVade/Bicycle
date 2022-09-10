from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BicycleSerializer
from .models import Bicycle


# Create your views here.

class BicyclesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BicycleSerializer
    queryset = Bicycle.objects.all()
