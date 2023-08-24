from django.shortcuts import render, get_object_or_404 
from rest_framework import generics, exceptions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MenuItem, Cart, Order, OrderItem,Category
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemsSerializer,CategorySerializer
from django.contrib.auth.models import User, Group
from .pagination import CustomPagination
# Create your views here.

class MenuItemsList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['category__title','title']
    ordering_fields = ['price', 'category']
    ordering = ['category']  # default ordering
    filterset_fields = ['price']
    pagination_class = CustomPagination
    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return super().perform_create(serializer)
        else: 
            raise exceptions.PermissionDenied
 
class MenuItemsRetrieveDestroyUpdate(generics.RetrieveDestroyAPIView, generics.UpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def perform_destroy(self, instance):
        if not self.request.user.groups.filter(name='Manager').exists():
            raise exceptions.PermissionDenied
        else:
            return super().perform_destroy(instance)
    def perform_update(self, serializer):
        if  self.request.user.groups.filter(name='Manager').exists() or  self.request.user.is_superuser:
            return super().perform_update(serializer)
        else:
            raise exceptions.PermissionDenied


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ManagersManagementListCreate(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager') or request.user.is_superuser:
            manager_users = User.objects.filter(groups__name='Manager')
            if manager_users:
                serialzed_items = UserSerializer(manager_users, many=True)
                return Response({"managers" : serialzed_items.data}, status=status.HTTP_200_OK)
            else: 
                return Response({'message':'no sush user'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            
            return Response({"error":"you have no permssion"}, status=status.HTTP_403_FORBIDDEN)
        
    elif request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            username = request.data.get('username')
            if username:
                user_to_add = get_object_or_404(User, username=username)
                manager_group = Group.objects.get(name='Manager')
                manager_group.user_set.add(user_to_add)
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
@api_view(['DELETE'])  
@permission_classes([IsAuthenticated])
def ManagersManagementDelete(request, pk):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        user = get_object_or_404(User, id=pk)
        if user:
            if not user.groups.filter(name = 'Manager'):
                return Response({'message':'no such user in manager group'}, status.HTTP_404_NOT_FOUND)
            manager_group = Group.objects.get(name = 'Manager')
            manager_group.user_set.remove(user)
            return Response({'message':'OK'}, status.HTTP_200_OK)
        #else:                        '''''NO NEED FOR THAT get_object_or_404 WILL DO IT FOR US'''
        #    return Response({'message':'no such registered user'}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def DeliveryCrewManagementListCreate(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            delivery_crew_users = User.objects.filter(groups__name='Delivery Crew')
            if delivery_crew_users:
                serialized_items = UserSerializer(delivery_crew_users, many=True)
                return Response({"delivery_crew": serialized_items.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'no delivey crew users'}, status=status.HTTP_200_OK)
        else :
            return Response({'message':'not authorised'}, status=status.HTTP_403_FORBIDDEN)
        
    elif request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            username = request.data.get('username')
            if username:
                user_to_add = get_object_or_404(User, username=username)
                delivery_crew_group = Group.objects.get(name='Delivery Crew')
                delivery_crew_group.user_set.add(user_to_add)
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeliveryCrewManagementDelete(request, pk):
    if request.user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User, id=pk)

        if not user.groups.filter(name='Delivery Crew').exists():
            return Response({'message': 'User is not in Delivery Crew'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            delivery_crew_group = Group.objects.get(name='Delivery Crew')
            delivery_crew_group.user_set.remove(user)
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'message': 'Delivery Crew group does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    
    

class CartMenuItemsListCreate(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user__id=user.id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class CartMenuItemsDelete(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            
        

from rest_framework import status

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message": "no item in cart"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        
        if order_serializer.is_valid():
            order = order_serializer.save()

            items = Cart.objects.filter(user=self.request.user)
            for item in items:
                orderitem = OrderItem(
                    order=order,
                    menu_item=item.menu_item,
                    price=item.price,
                    quantity=item.quantity,
                )
                orderitem.save()

            Cart.objects.filter(user=self.request.user).delete()  # Delete cart items
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.filter(user=user)
        for item in items:
            total += item.price
        return total

    
    
    
class OrderRetrieveUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def retrieve(self, request, pk):
        order = self.get_object()
        order_id = order.id
        # Dilevery Crew and Manager users would be able to see and check 
        if order.user != self.request.user and not self.request.user.groups.filter(name='Manager'):
            return Response({"message":'unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        query_set = OrderItem.objects.filter(order__id=order_id)
        items = []
        for obj in query_set:
            items.append({
                "id": obj.id,
                "menu_item": obj.menu_item.title,
                "quantity": obj.quantity,
                "unit_price": obj.unit_price,
                "price": obj.price
            })
        
        return Response({f"order {pk} menu items": items}, status=status.HTTP_200_OK)
            
        
    def perform_update(self, serializer):
        if self.request.user.groups.filter(name='Delivery Crew').exists():
            stat = serializer.validated_data.get('status')
            try:
                serializer.save(status=stat)
            except Exception as e:  
               return Response({"message": f"Error: {str(e)}"})
        
        elif self.request.user.groups.filter(name='Manager').exists():
            delivery_crew = serializer.validated_data.get('delivery_crew')
            status = serializer.validated_data.get('status')
            saved_data = {} 
            if delivery_crew :
                saved_data['delivery_crew'] = delivery_crew
            if status :
                saved_data['status'] = status
                
            if saved_data:
                serializer.save(**saved_data)
        else : raise exceptions.PermissionDenied('you do not have permission!')
    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Manager').exists():
            instance.delete()
        else:
            raise exceptions.PermissionDenied('You do not have permission to')
        
class CategoryAdminADD(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return super().perform_create(serializer)
        else: 
            raise exceptions.PermissionDenied