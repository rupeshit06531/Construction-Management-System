from django.urls import path

from .views import (
    DashboardReportAPIView,
    ReportDetailAPIView,
    ReportListCreateAPIView,
)


urlpatterns = [
    path(
        "dashboard/",
        DashboardReportAPIView.as_view(),
        name="dashboard-report",
    ),
    path(
        "",
        ReportListCreateAPIView.as_view(),
        name="report-list-create",
    ),
    path(
        "<int:pk>/",
        ReportDetailAPIView.as_view(),
        name="report-detail",
    ),
]