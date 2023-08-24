from django.urls import path
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemsList.as_view()),
    path("menu-items/<int:pk>", views.MenuItemsRetrieveDestroyUpdate.as_view()),
    path("groups/manager/users", views.ManagersManagementListCreate),
    path("groups/manager/users/<int:pk>", views.ManagersManagementDelete),
    path("groups/delivery-crew/users", views.DeliveryCrewManagementListCreate),
    path("groups/delivery-crew/users/<int:pk>", views.DeliveryCrewManagementDelete),
    path("cart/menu-items", views.CartMenuItemsListCreate.as_view()),
    path("cart/menu-items/<int:pk>", views.CartMenuItemsDelete.as_view()),
    path("orders", views.OrderListCreate.as_view()),
    #path("orders/<int:pk", views.OrderMenuItemsList.as_view()),
    path("orders/<int:pk>", views.OrderRetrieveUpdateDestroy.as_view()),
    #path("orders/<int:pk>", views.OrderDelete.as_view()),
    path("categories", views.CategoryAdminADD.as_view()),
    
]