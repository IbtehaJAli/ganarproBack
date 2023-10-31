from unicodedata import decimal

from django.http import Http404, JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.mortgage_calculator.models import PricingModel, StateLaborPrice, CleanUPEstimates
from app.api.mortgage_calculator.serializers import BidAmountPricingModelSerializer, StateLaborPricingModelSerializer, \
    CleanUPEstimatesSerializer
from app.api.users.permissions import IsOwner


# Create your views here.
class BidAmountPricingModelDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = BidAmountPricingModelSerializer
    queryset = PricingModel.objects.all()

    def get(self, request, project_type, format=None):
        try:
            phase = self.request.query_params.get('phase')
            if phase in ['rough_final', 'final_rough']:
                phase = 'rough_final'
            elif phase in ['rough_fluff', 'fluff_rough']:
                phase = 'rough_fluff'
            elif phase in ['final_fluff', 'fluff_final']:
                phase = 'final_fluff'
            elif phase in {'rough_final_fluff', 'rough_fluff_final', 'final_fluff_rough', 'fluff_rough_final',
                           'final_rough_fluff', 'fluff_final_rough'}:
                phase = 'rough_final_fluff'
            pricing_model = PricingModel.objects.get(project_type=project_type)
            serializer = BidAmountPricingModelSerializer(pricing_model)
            amount = PricingModel.objects.filter(project_type=project_type).values_list(phase, flat=True)[0]
            return Response({'phase': phase, 'amount': float(amount), 'data':serializer.data }, status=status.HTTP_200_OK)

        except PricingModel.DoesNotExist:
            raise Http404
    # return Response(serializer.data)


class BidAmountPricingModelListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BidAmountPricingModelSerializer

    def get_queryset(self):
        return PricingModel.objects.all()



class StateLaborPricingModelDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = StateLaborPricingModelSerializer
    queryset = StateLaborPrice.objects.all()

    def get_object(self):
        state = self.kwargs['state']
        try:
            return StateLaborPrice.objects.get(area_name=state)
        except StateLaborPrice.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        state_labor = self.get_object()
        serializer = StateLaborPricingModelSerializer(state_labor)
        return Response(serializer.data)


class StateLaborPricingModelListCreateAPI(generics.ListCreateAPIView):
    serializer_class = StateLaborPricingModelSerializer

    def get_queryset(self):
        return StateLaborPrice.objects.all()


class CleanUPEstimateListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CleanUPEstimatesSerializer

    def get_queryset(self):
        return CleanUPEstimates.objects.filter(user=self.request.user).order_by("-modified")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        # serializer.context["user_id"] = request.user.id
        if serializer.is_valid(raise_exception=True):
            # create_proposal_template(request.data)
            request.user.profile.free_mode_action = request.user.profile.free_mode_action + 1 \
                if request.user.profile.free_mode_action < 10 else 10
            request.user.profile.save()
            serializer.save(user=request.user)
            return_message = {
                "message": "CleanUPEstimates created successfully",
                "data": serializer.data,
            }

            return Response(return_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleanUPEstimateDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = CleanUPEstimatesSerializer
    queryset = CleanUPEstimates.objects.all()
    permission_classes = (IsOwner, IsAuthenticated)

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return CleanUPEstimates.objects.get(pk=pk, user=self.request.user)
        except CleanUPEstimates.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        estimates = self.get_object()
        serializer = CleanUPEstimatesSerializer(estimates)
        return Response(serializer.data)


def get_calculation_info(request):
    pricing_data = PricingModel.objects.only('project_type', 'final')
    pricing_list = [{'project_type': entry.project_type, 'final': entry.final} for entry in pricing_data]
    state_data = StateLaborPrice.objects.only('area_name', 'price_customer', 'one_day_work', 'percentage')
    state_list = [{'area_name': entry.area_name, 'price_customer': entry.price_customer, 'one_day_work': entry.one_day_work, 'percentage':entry.percentage} for entry in state_data]
    data = {
        'pricing_data': pricing_list,
        'state_data': state_list
    }
    return JsonResponse(data)