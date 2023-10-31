import io
import json
import os
from wsgiref.util import FileWrapper

import djstripe
import stripe
from django.http import Http404, HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from docx import Document
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from app.api.authentication.models.user_registration import UserProfile
from app.api.gc_planify.serializers import GeneralContractorsSerializer
from app.api.project_type.models import ProjectType
from app.api.proposal.helpers import create_proposal_template
from app.api.proposal.models import Proposal
from app.api.proposal.serializers import ProposalSerializer
from app.api.users.permissions import IsOwner
from app.api.users.serializers import UserProfileSerializer


class ProposalListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        return Proposal.objects.filter(user=self.request.user).order_by("-modified")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        project_type = get_object_or_404(ProjectType, name=request.data['project_type'])

        # serializer.context["user_id"] = request.user.id
        if serializer.is_valid(raise_exception=True):
            # create_proposal_template(request.data)
            request.user.profile.free_mode_action = request.user.profile.free_mode_action + 1 \
                if request.user.profile.free_mode_action < 10 else 10
            request.user.profile.save()
            serializer.save(user=request.user, project_type=project_type)
            return_message = {
                "message": "Proposal created successfully",
                "data": serializer.data,
            }

            return Response(return_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProposalDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.all()
    permission_classes = (IsOwner, IsAuthenticated)

    def get_object(self, pk):
        try:
            return Proposal.objects.get(id=pk)
        except Proposal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        proposal = self.get_object(pk)
        serializer = ProposalSerializer(proposal)
        return Response(serializer.data)

    #

    def put(self, request, pk, format=None):
        proposal = self.get_object(pk)
        if isinstance(request.data['project_type'], str):
            project_type = request.data['project_type']
            project_type = get_object_or_404(ProjectType, name=project_type)
        else:
            project_type = request.data['project_type']
            project_type = get_object_or_404(ProjectType, id=project_type)

        serializer = ProposalSerializer(proposal, data=request.data)
        if serializer.is_valid():
            serializer.save(project_type=project_type)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        proposal = self.get_object(pk)
        proposal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def proposal_download(request, pk):
    if pk == 0:

        data = request.data
        project_type = ProjectType.objects.get(name=data['project_type'])
        data['template'] = project_type.template
        data['project_type'] = {'slug': project_type.slug, 'name': project_type.name}
        create_proposal_template(data)
    else:
        proposal = Proposal.objects.get(pk=pk, user=request.user)
        serializer = ProposalSerializer(proposal)
        serializer_data = serializer.data
        serializer_data['template'] = proposal.project_type.template
        create_proposal_template(serializer_data)

    # serializer.save(user=request.user)
    document = open('documents/mergedv1.docx', 'rb')
    #
    # response = HttpResponse(document, content_type='text/plain')
    # response['Content-Disposition'] = 'attachment; filename=CleanUPProposal.txt'

    # document = Document()
    #
    # # save document info
    buffer = io.BytesIO()
    # document.save(buffer)  # save your memory stream
    document.seek(0)  # rewind the stream

    # put them to streaming content response
    # within docx content_type
    response = StreamingHttpResponse(
        streaming_content=document,  # use the stream's content
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    response['Content-Disposition'] = 'attachment;filename=CleanUpProposal.docx'
    response["Content-Encoding"] = 'UTF-8'
    # with open('test.xlsx', 'rb') as fh:
    #     response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
    #     response['Content-Disposition'] = 'inline; filename=' + os.path.basename('test.xlsx')
    #     return response
    # return_message = {
    #     "message": "Proposal created successfully",
    #     "data": serializer.data,
    # }

    return response


@api_view(['POST'])
def subscriptions(request):
    # Reads application/json and returns a response
    data = request.data
    payment_method = data['payment_method']
    price_id = data['price_id']
    first_name = data['first_name']
    last_name = data['last_name']
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)
    customer_data = stripe.Customer.list(email=data['email']).data

    try:
        # This creates a new Customer and attaches the PaymentMethod in one API call.
        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                name=f"{first_name} {last_name}",
                payment_method=payment_method,
                email=data['email'],
                invoice_settings={
                    'default_payment_method': payment_method
                },

            )
        else:
            customer = customer_data[0]

        djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

        if request.user.user_type == "CLN":
            request.user.profile.customer = djstripe_customer
        else:
            request.user.general_contractor.customer = djstripe_customer

        # At this point, associate the ID of the Customer object with your
        # own internal representation of a customer, if you have one.
        # Subscribe the user to the subscription created ,
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": price_id,
                },
            ],
            expand=["latest_invoice.payment_intent"],
            metadata={"price_id": price_id}
        )
        djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

        if request.user.user_type == "CLN":

            request.user.profile.subscription = djstripe_subscription
            request.user.profile.save()
            serializer = UserProfileSerializer(instance=request.user.profile)
        else:
            request.user.general_contractor.subscription = djstripe_subscription
            request.user.general_contractor.save()
            serializer = GeneralContractorsSerializer(instance=request.user.general_contractor)

        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status=403)
