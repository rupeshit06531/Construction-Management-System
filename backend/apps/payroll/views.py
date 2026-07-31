from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Payroll
from .serializers import PayrollSerializer


class PayrollViewSet(ModelViewSet):

    queryset = Payroll.objects.all().order_by("-created_at")

    serializer_class = PayrollSerializer

    permission_classes = [
        IsAuthenticated,
    ]