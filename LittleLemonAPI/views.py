from django.contrib.auth.models import User, Group

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import (
    MenuItem,
    Cart,
    Order,
    OrderItem,
)
from .serializers import (
    MenuItemSerializer,
    UserSerializer,
    CartSerializer,
    OrderSerializer,
)
from .permissions import IsManager, IsDeliveryCrew


class MenuItemView(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    ordering_fields = ['price']
    search_fields = ['title']
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
        return [permission() for permission in permission_classes]            
    
    
class DetailItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        
        if self.request.method == 'POST' \
                or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' \
                or self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
        
        return [permission() for permission in permission_classes]
    
    
class ManagerUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    
    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        return User.objects.filter(groups=manager_group)
    
    def perform_create(self, serializer):
        manager_group = Group.objects.get(name='Manager')
        user = serializer.save()
        user.groups.add(manager_group)


class ManagerUserDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    
    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        return User.objects.filter(groups=manager_group)
    
    
class DeliveryCrewUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsDeliveryCrew]
    
    def get_queryset(self):
        manager_group = Group.objects.get(name='Delivery crew')
        return User.objects.filter(groups=manager_group)
    
    def perform_create(self, serializer):
        manager_group = Group.objects.get(name='Delivery crew')
        user = serializer.save()
        user.groups.add(manager_group)


class DeliveryCrewDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsDeliveryCrew]
    
    def get_queryset(self):
        manager_group = Group.objects.get(name='Delivery crew')
        return User.objects.filter(groups=manager_group)


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def perform_create(self, serializer):
        menuitem = self.request.data.get('menuitem')
        quantity = int(self.request.data.get('quantity'))
        unit_price = MenuItem.objects.get(pk=menuitem).price
        price = quantity * unit_price
        serializer.save(user=self.request.user, price=price)


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists:
            return Order.objects.all()
        return Order.objects.filter(user=user)
            
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price,
                order=order,
            )
            cart_item.delete()
        
    def calculate_total(self, cart_items):
        total = 0
        for item in cart_items:
            total += item.price
        return total
        

class DetailOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists:
            return Order.objects.all()
        return Order.objects.filter(user=user)