from rest_framework.routers import DefaultRouter # ειναι κλαση , (καλουπι) 
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet,CheckoutView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView )
from django.urls import path

router = DefaultRouter() # αντικειμενο router που φτιαχνει αυτοματα τα urls, που κληρονομει απο τα εργαλεια των ViewSet
router.register(r'categories',CategoryViewSet)
router.register(r'products',ProductViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'order-items',OrderItemViewSet)
router.register(r'carts',CartViewSet)
router.register(r'cart-items',CartItemViewSet)
# router.register(r'checkout',CheckoutViewSet) δεν γινεται κατι , γιατι ειναι APIview , δηλαδη custom 

urlpatterns =  router.urls + [
    path('checkout/',CheckoutView.as_view(),name='checkout'), # δεν χρησιμοποιηουμε το αντικειμενο router των ModelVieSet , 
                                                                 # οποτε πρεπει να καλεσουμε την συναρτηση .as_view() για να εχουμε το σωστο url
]
#     path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
#     path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
 