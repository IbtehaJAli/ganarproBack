import djstripe
import stripe
from django.db import transaction
from django.http import Http404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from djstripe.models import Subscription
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, generics

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsOwner
from .serializers import UserSerializer, RegisterUserSerializer, UserProfileSerializer
from ..authentication.models import User
from ..authentication.models.user_registration import UserProfile
from ..authentication.serializers.user_login import CustomTokenObtainPairSerializer
from djstripe.models import Subscription

from ..gc_planify.serializers import GeneralContractorsSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            status_code = status.HTTP_201_CREATED
            refresh = RefreshToken.for_user(user.user)
            if request.data.get('is_gc', False):
                profile = GeneralContractorsSerializer(user).data
            else:
                profile = UserProfileSerializer(user).data


            response = {
                'message': 'User registered  successfully',
                'data': profile,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(response, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    # permission_classes = (IsAuthenticated, IsAdminUser)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    parser_classes = [MultiPartParser]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'user_id': self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        request_data = dict(request.data.lists())
        serializer = UserProfileSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_free_mode_action(request):
    request.user.profile.free_mode_action = request.user.profile.free_mode_action + 1 \
        if request.user.profile.free_mode_action < 10 else 10
    request.user.profile.save()
    return Response({'free_mode_count': request.user.profile.free_mode_action}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def customer_portal(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Authenticate your user.
    customer = request.data
    session = stripe.billing_portal.Session.create(
        customer=customer,
        return_url=settings.BASE_URL,
    )
    return Response({"session_url": session.url})


# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'sk_test_26PHem9AhJZvU623DfE1x4sd'


@api_view(['POST'])
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY  # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    # request_data = json.loads(request.data)
    stripe.api_key = "sk_test_51MVRmbFoZLegDZsX90BlVOWiZqA3XPtqFXIAyckMAKshoPJDyC1H1OwgH0aFXYMLtqgKFTwm0oTNDmFTcJXrtSEz007Qw6CxLk"

    # This is your Stripe CLI webhook secret for testing your endpoint locally.
    webhook_secret = 'whsec_1f94e7336011e137d54afb1142b63ec3d6fcd27e91b2166229d2667d0b25e193'

    # if webhook_secret:
    #     # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    #     signature = request.headers.get('stripe-signature')
    #     try:
    #         event = stripe.Webhook.construct_event(
    #             payload=request.data, sig_header=signature, secret=webhook_secret)
    #         data = event['data']
    #     except Exception as e:
    #         return e
    #     # Get the type of webhook event sent - used to check the status of PaymentIntents.
    #     event_type = event['type']
    # else:
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    payload = request.body
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    data = event['data']['object']
    if event['type'] == 'customer.created':
        email = data['email']
        #
        try:

            user_profile = User.objects.get(email=email).profile
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(data)
            user_profile.customer = djstripe_customer
            user_profile.save()
        except User.DoesNotExist:
            # create user
            user = User.objects.create(
                email=email
            )
            user.set_password('G$N4PR0^')
            user.save()

            # create profile
            user_profile = UserProfile.objects.create(
                user=user,
                first_name='test',
                last_name='test',
                phone='test',
                address='test',
            )
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(data)
            user_profile.customer = djstripe_customer
            user_profile.save()




        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.

    if event['type'] == 'customer.subscription.updated':
        customer = stripe.Customer.retrieve(data['customer'])
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": "price_1Ms6oZFoZLegDZsXgZwClUPZ",
                },
            ],
        )
        djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

        request.user.profile.subscription = djstripe_subscription
        request.user.profile.save()
        # user_profile = djstripe.models.Customer.objects.get(id=customer['id']).profile
        # djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(data)
        # user_profile.subscription = djstripe_subscription
        # user_profile.save()

        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.

    if event['type'] == 'invoice.paid':

        # djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
        # request.user.profile.customer = djstripe_customer
        # Used to provision services after the trial has ended.
        # The status of the  vinvoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # print(data)
        pass

    if event['type'] == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        # print(data)
        pass

    if event['type'] == 'customer.subscription.deleted':
        # handle subscription canceled automatically based
        # upon your subscription settings. Or if the user cancels it.
        pass
        # print(data)

    return HttpResponse(status=200)
