from django.urls import path

from .views import AboutView, ContactsView, IndexView, RobotsTxtView


app_name = "core"


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("robots.txt", RobotsTxtView.as_view(), name="robots"),
]

