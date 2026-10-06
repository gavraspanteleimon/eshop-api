from .models import Category, Product, Order, OrderItem, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CheckoutView(APIView):    # κληρονομεί από την κλασση APIView: είναι "ένα είδος APIView"
    def post(self, request):    # ονομα συναρτησης - τρέχει όταν έρθει POST request - για αυτο ονομαζεται το ιδιο
                                # self = το συγκεκριμένο αντικείμενο (instance) του CheckoutView που χειρίζεται αυτό το request 
                                # request = το πακέτο που μας δίνει έτοιμο το DRF( περιεχει headers, body με το json που έστειλε ο client, κλπ)
                               
        # ---- Βήμα 1: βρες τον χρήστη ----
        user_id = request.data.get('user_id')   # request.data = dictionary με το JSON που έστειλε ο client ,ειναι το payload  sto network request, 
                                                # .get('user_id') = σου δινουμε το key user_id, 
                                                # θελουμε να μας επιστρεψεις το value   (ή None αν δεν υπάρχει)   , δεν το επιστρεφει το μεταφραζει εκεινη την στιγμη και το βάζει στην μεταβλητή user_id       
        try:                                    # "δοκίμασε να κάνεις αυτό..."
            current_user = User.objects.get(id=user_id) #User , κλαση μοντελο django απο import, αντιστοιχει στον πινακαauth_user της βασης
                                                #.objects = ο διαχειριστής του μοντέλου (Model Manager) που μας δίνει έτοιλες συναρτήσεις για να κάνουμε queries στη βάση(.all(), .get(), .filter(), κλπ)
                                                #.g# .get('user_id') = ψάχνει το key user_id και ΕΠΙΣΤΡΕΦΕΙ την τιμή του (ή None αν λείπει)
                                                # user_id = ...   = βάζει αυτή την τιμή στη δική μας μεταβλητή
        except User.DoesNotExist:               # "...και αν δεν υπάρχει τέτοιος χρήστης, μην κρασάρεις"
            return Response(                    # return = η συνάρτηση σταματάει εδώ και απαντάμε στον client
                {"error": "User does not exist with the provided user_id."},   # το μήνυμα
                status=status.HTTP_404_NOT_FOUND                                # 404 = δεν βρέθηκε
            )

        # ---- Βήμα 2: πάρε το Cart του χρήστη ----
        # Εδώ ξέρουμε σίγουρα ότι ο user υπάρχει (αλλιώς θα είχαμε φύγει με return παραπάνω)
        try:
            my_cart = Cart.objects.get(user=current_user)  # Cart            = κλάση/μοντέλο (πίνακας eshop_cart)
                                                # .objects        = ο model manager (χαρακτηριστικό, χωρίς παρενθέσεις)
                                                # .get(user=current_user) = φέρε τη ΜΙΑ γραμμή του πίνακα όπου η στήλη user ταιριάζει με τον user του Βήματος 1
                                                # my_cart (μικρό)    = η δική μας μεταβλητή που κρατάει το αντικείμενο Cart που βρέθηκε
                                              
        except Cart.DoesNotExist:               # ο χρήστης μπορεί να υπάρχει χωρίς καλάθι
            return Response(
                {"error": "This user has no cart."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # TODO Βήμα 3: πάρε τα CartItems του cart
        
        cart_items = CartItem.objects.filter(cart = my_cart) # cart_items = η μεταβλητη μας που περιεχει ολα τα items του my_cart
                                                             # CartItem            = κλάση/μοντέλο (πίνακας eshop_cartitem)
                                                             # .objects            = ο model manager
                                                             # .filter(cart=my_cart)  = φέρε ΟΛΕΣ τις γραμμές όπου η στήλη cart ταιριάζει με το cart του Βήματος 2
                                                             # αριστερό cart = όνομα στηλης στον πινακα CartItem (το ForeignKey)
                                                             # δεξί my_cart     = η μεταβλητή που φτιάξαμε στο Βήμα 2

        # TODO Βήμα 4: αν είναι άδειο, return Response({"error": "..."}, status=status.HTTP_400_BAD_REQUEST)
        if not cart_items:
            return Response({"error" : "There are no items in the cart"},status=status.HTTP_400_NOT_FOUND)
                        
        # TODO Βήμα 5 : υπολόγισε total
        cart_total = 0 
        for item in cart_items:
            cart_totaltotal = cart_totaltotal + item.quantity * item.product.price 

        # TODO Βήμα 6 :  φτιάξε Order
        new_order = Order.objects.create(user=current_user , total=cart_total) #φτιαχνει στον model- πινακα ORDER , την στηλη-πεδιο με key user , και value to username απο το βημα 1
                                                                                # φτιαχνει αντιστοιχα την στηληπεδιο με key total , και value to cart_total apo to βημα 5
        # TODO Βήμα 7: loop στα cart items, φτιάξε OrderItem για το καθένα
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=cart_item.product,
                quantity= cart_item.quantity,
                unit_price=cart_item.product.price
            )

        # TODO Βήμα 8: άδειασε το cart
        cart_items.delete()

        # TODO Βήμα 9: return Response(...)
        serializer = OrderSerializer(new_order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)