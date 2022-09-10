from django.urls import path
from . import views

urlpatterns = [
    path("", views.BicyclesView.as_view(), name="bicycles_list_and_create"),

]
