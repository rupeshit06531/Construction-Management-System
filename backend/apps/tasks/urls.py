from django.urls import path

from .views import (
    TaskDetailAPIView,
    TaskListCreateAPIView,
)


urlpatterns = [
    path(
        "",
        TaskListCreateAPIView.as_view(),
        name="task-list-create",
    ),
    path(
        "<int:pk>/",
        TaskDetailAPIView.as_view(),
        name="task-detail",
    ),
]