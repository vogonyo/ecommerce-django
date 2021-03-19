from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home , name="home"),
    path('store/', views.store , name="store"),
    path('about/', views.about , name="about"),
    path('category/sutures', views.sutures , name="sutures"),
    path('category/labware', views.labware , name="labware"),
    path('category/equipment', views.equipment , name="equipment"),
    path('category/instruments', views.instruments , name="instruments"),
    path('category/culture', views.culture , name="culture"),
    path('category/media', views.media , name="media"),
    path('contact/', views.contact , name="contact"),
    path('cart/', views.cart , name="cart"),
    path('checkout/', views.checkout , name="checkout"),
    path('update_item/', views.updateItem , name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]