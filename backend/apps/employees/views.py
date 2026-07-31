from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateAPIView(generics.ListCreateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]