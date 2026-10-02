from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView )
from django.urls import path

router = DefaultRouter()
router.register(r'categories',CategoryViewSet)
router.register(r'products',ProductViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'order-items',OrderItemViewSet)
router.register(r'carts',CartViewSet)
router.register(r'cart-items',CartItemViewSet)

urlpatterns =  router.urls
#     path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
#     path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
 