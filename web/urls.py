from django.contrib import admin
from django.urls import path
from. import views


urlpatterns = [

    path('',views.index),
    path('view_product_details/<str:category>/',views.product_details_view),
    path('cart/',views.cart),
    path('checkout/',views.checkout),
    path('order_send_to_whatsaapp/<str:name>/<str:address>/<str:phone>/',views.send_to_whatsapp),
    path('about/',views.about),
    path('contact/',views.contact),
    path('search/',views.search_items),
]
