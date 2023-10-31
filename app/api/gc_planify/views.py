from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.gc_planify.models import GeneralContractor
from app.api.gc_planify.serializers import GeneralContractorsSerializer
from app.api.users.permissions import IsOwner
from app.api.utils.renderers import RequestJSONRenderer


class GeneralContractorRetrieve(generics.RetrieveAPIView):
    serializer_class = GeneralContractorsSerializer
    queryset = GeneralContractor.objects.all()
    renderer_classes = (RequestJSONRenderer,)
    lookup_field = 'company_slug'
    permission_classes = (IsOwner, IsAuthenticated)

    # parser_classes = [MultiPartParser]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        if self.request.user.is_authenticated:
            filter_kwargs = {'user_id': self.request.user.id}
            obj = get_object_or_404(queryset, **filter_kwargs)
        else:
            filter_kwargs = {'company_slug': self.kwargs.get('company_slug')}
            obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        print('HERE')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return_message = {
            "message": "Fetch details successfully",
            "data": serializer.data,
        }
        return Response(return_message, status=status.HTTP_200_OK)


class GeneralContractorRetrieveUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GeneralContractorsSerializer
    queryset = GeneralContractor.objects.all()
    renderer_classes = (RequestJSONRenderer,)
    lookup_field = 'company_slug'
    # permission_classes = (IsOwner, IsAuthenticated)

    # parser_classes = [MultiPartParser]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.

        """
        queryset = self.filter_queryset(self.get_queryset())
        print(self.request.user)

        filter_kwargs = {'user_id': self.request.user.id}
        print(filter_kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = GeneralContractorsSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return_message = {
                "message": "Update details successfully",
                "data": serializer.data,
            }
            return Response(return_message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
