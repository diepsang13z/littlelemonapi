from django.urls import path

from .views import (
    MenuItemView, 
    DetailItemView,
    ManagerUserView,
    ManagerUserDeleteView,
    DeliveryCrewUserView,
    DeliveryCrewDeleteView,
    CartView,
    OrderView,
    DetailOrderView,
)


urlpatterns = [
    path('menu-items/', MenuItemView.as_view()),
    path('menu-items/<int:pk>/', DetailItemView.as_view()),
    path('groups/manager/users/', ManagerUserView.as_view()),
    path('groups/manager/users/<int:pk>', ManagerUserDeleteView.as_view()),
    path('groups/delivery-crew/users/', DeliveryCrewUserView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', DeliveryCrewDeleteView.as_view()),
    path('cart/menu-items/', CartView.as_view()),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>', DetailOrderView.as_view()),
]
