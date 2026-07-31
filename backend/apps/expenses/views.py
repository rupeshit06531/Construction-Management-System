from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(ModelViewSet):

    queryset = Expense.objects.all().order_by("-created_at")

    serializer_class = ExpenseSerializer

    permission_classes = [
        IsAuthenticated,
    ]