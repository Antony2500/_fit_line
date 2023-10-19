from django.urls import path
from . import views

urlpatterns = [
    path("make_order/", views.order, name='make_order'),
]
