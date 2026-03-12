from django.urls import path

from .views import ApplyView


app_name = "applications"


urlpatterns = [
    path("", ApplyView.as_view(), name="apply"),
]

