from django.urls import path
from . import views
from . import Login
from .ProductList import analyze_product_image


urlpatterns = [
    path("login/", views.login, name="login"),
   path("user/<int:user_id>/", views.get_user, name="get_user"),
    path("analyze-image/", analyze_product_image, name="analyze_product_image"),
    path("products/", views.get_products, name="get_products"),
]
