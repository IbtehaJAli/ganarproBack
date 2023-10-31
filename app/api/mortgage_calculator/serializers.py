from rest_framework import serializers

from app.api.mortgage_calculator.models import PricingModel, StateLaborPrice, CleanUPEstimates


class BidAmountPricingModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = PricingModel
        fields = '__all__'


class StateLaborPricingModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = StateLaborPrice
        fields = '__all__'



class CleanUPEstimatesSerializer(serializers.ModelSerializer):


    class Meta:
        model = CleanUPEstimates
        fields = '__all__'
