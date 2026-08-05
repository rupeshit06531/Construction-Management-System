from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.select_related(
        "employee",
    ).order_by("-date", "-created_at")

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated,
    ]


class AttendanceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.select_related(
        "employee",
    )

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated,
    ]