from django.urls import path

from .views import CatalogIndexView, CategoryView, ProductView


app_name = "catalog"


urlpatterns = [
    path("", CatalogIndexView.as_view(), name="index"),
    path("<slug:category_slug>/", CategoryView.as_view(), name="category"),
    path("<slug:category_slug>/<slug:product_slug>/", ProductView.as_view(), name="product"),
]

