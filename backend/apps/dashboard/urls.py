from django.urls import path

from .views import DashboardKPIAPIView


urlpatterns = [
    path(
        "kpi/",
        DashboardKPIAPIView.as_view(),
        name="dashboard-kpi",
    ),
]