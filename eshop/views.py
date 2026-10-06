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


# --- Imports: από πού έρχονται τα ονόματα που χρησιμοποιούμε ---
from rest_framework.views import APIView        # η "βάση" από την οποία κληρονομεί η view μας
from rest_framework.response import Response    # για να στέλνουμε απάντηση στον client
from rest_framework import status               # έτοιμοι HTTP κωδικοί (404, 400, 201...)
from django.contrib.auth.models import User     # το μοντέλο των χρηστών του Django
from .models import Cart, CartItem, Order, OrderItem   # τα δικά μας μοντέλα
from .serializers import OrderSerializer        # μετατρέπει ένα αντικείμενο Order σε JSON για την απάντηση


class CheckoutView(APIView):    # κληρονομεί από την κλασση APIView: η Checkoutview είναι "ένα είδος APIView"
    def post(self, request):    # ονομα συναρτησης - τρέχει όταν έρθει POST request - για αυτο ονομαζεται το ιδιο
                                # self = το συγκεκριμένο αντικείμενο (instance) του CheckoutView που χειρίζεται αυτό το request
                                # request = το πακέτο που μας δίνει έτοιμο το DRF( περιεχει headers, body με το json που έστειλε ο client, κλπ)

        # ---- Βήμα 1: βρες τον χρήστη ----
        user_id = request.data.get('user_id')   # request.data = dictionary με το JSON που έστειλε ο client ,ειναι το payload  sto network request,
                                                # .get('user_id') = σου δινουμε το key user_id, και θελουμε να επιστρεψεις το value της μεταβλητης user_id
                                                # θελουμε να μας επιστρεψεις το value   (ή None αν δεν υπάρχει)   
        try:                                    # "δοκίμασε να κάνεις αυτό..."
            current_user = User.objects.get(id=user_id) #User , κλαση μοντελο django απο import, αντιστοιχει στον πινακα auth_user της βασης
                                                #.objects = ο διαχειριστής του μοντέλου (Model Manager) που μας δίνει έτοιλες συναρτήσεις για να κάνουμε queries στη βάση(.all(), .get(), .filter(), κλπ)
                                                # το id στα αριστερα ειναι το ονομα στηλης στον πίνακα user , 
                                                # user_id = ...   = είναι το value που εστειλε πριν με το response o client , 
                                                # αποθηκευεται όλο στην νεο αντικειμενο που φτιαξαμε το current_user 
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
                                                # .get(user=current_user) = φέρε τη ΜΙΑ γραμμή του πίνακα όπου η στήλη user ταιριάζει με τον current_user του Βήματος 1
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
                                                             # .filter(cart=my_cart)  = φέρε ΟΛΕΣ τις γραμμές όπου η στήλη cart απο τον πινακα της βασης ταιριάζει με το my_cart του Βήματος 2
                                                             # αριστερό cart = όνομα στηλης στον πινακα CartItem (το ForeignKey)
                                                             # δεξί my_cart     = η μεταβλητή που φτιάξαμε στο Βήμα 2

        # ---- Βήμα 4: αν το καλάθι είναι άδειο, σταματάμε ----
        if not cart_items:                      # QuerySet χωρίς γραμμές => "άδεια λίστα" => not [] => True
            return Response(
                {"error": "There are no items in the cart"},   # το μήνυμα για τον client
                status=status.HTTP_400_BAD_REQUEST             # 400 = το αίτημα δεν γίνεται δεκτό (checkout με άδειο καλάθι)
            )
        # Από εδώ και κάτω ξέρουμε σίγουρα ότι υπάρχουν ο user, το cart ΚΑΙ τουλάχιστον ένα item

        # ---- Βήμα 5: υπολόγισε το συνολικό ποσό ----
        ''
        cart_total = 0                          # ο "συσσωρευτής": ξεκινάμε από 0, ΠΡΙΝ το loop
        for cart_item in cart_items:            # για κάθε γραμμή του καλαθιού (ένα CartItem κάθε φορά)...
            cart_total = cart_total + cart_item.quantity * cart_item.product.price
                                                # cart_item.quantity      = η ποσότητα (πεδίο του CartItem)
                                                # cart_item.product       = ακολουθούμε το ForeignKey και παίρνουμε το αντικείμενο Product
                                                # cart_item.product.price = η τιμή του προϊόντος
                                                # ποσότητα × τιμή, και το προσθέτουμε στο σύνολο

        # ---- Βήμα 6: φτιάξε την Order ----
        new_order = Order.objects.create(user=current_user, total=cart_total)
                                                # .create(...) = ΓΡΑΦΕΙ μια νέα γραμμή στον πίνακα eshop_order (τα .get/.filter απλά διαβάζουν)
                                                # user=current_user  : στη στήλη user μπαίνει ο χρήστης του Βήματος 1 (στη βάση αποθηκεύεται το id του)
                                                # total=cart_total   : στη στήλη total μπαίνει το σύνολο του Βήματος 5
                                                # status και created_at συμπληρώνονται μόνα τους (default 'pending' και auto_now_add)
                                                # new_order = το αντικείμενο Order που μόλις φτιάχτηκε, θα το χρειαστούμε στο Βήμα 7

        # ---- Βήμα 7: ένα OrderItem για κάθε cart_item ----
        for cart_item in cart_items:            # ξανά loop στα items του καλαθιού (η Order υπάρχει πια, άρα μπορούμε να δείξουμε προς αυτήν)
            OrderItem.objects.create(           # σε κάθε γύρο γράφεται μία νέα γραμμή στον πίνακα eshop_orderitem
                order=new_order,                # σε ποια Order ανήκει (η ίδια σε όλες τις γραμμές)
                product=cart_item.product,      # ποιο προϊόν (μικρό p: όνομα πεδίου στο μοντέλο)
                quantity=cart_item.quantity,    # η ίδια ποσότητα που είχε το καλάθι
                unit_price=cart_item.product.price   # η τρέχουσα τιμή του προϊόντος: "κλειδώνει" στο OrderItem
            )

        # ---- Βήμα 8: άδειασε το καλάθι ----
        cart_items.delete()                     # σβήνει ΜΟΝΟ τα items αυτού του καλαθιού (το cart_items είναι ήδη φιλτραρισμένο)
                                                # ΠΡΟΣΟΧΗ: το CartItem.objects.all().delete() θα έσβηνε τα items ΟΛΩΝ των χρηστών
                                                # σε SQL: DELETE FROM eshop_cartitem WHERE cart_id = <το id του my_cart>

        # ---- Βήμα 9: επέστρεψε την Order στον client ----
        serializer = OrderSerializer(new_order)  # ο serializer μετατρέπει το αντικείμενο Order σε πεδία έτοιμα για JSON
        return Response(serializer.data, status=status.HTTP_201_CREATED)
                                                # serializer.data = το dictionary με τα πεδία της Order
                                                # 201 = Created: ο σωστός κωδικός όταν δημιουργείται κάτι νέο