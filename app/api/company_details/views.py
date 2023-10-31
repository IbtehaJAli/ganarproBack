# Create your views here.
from rest_framework import generics, views
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader
from rest_framework.response import Response
from ..authentication.models.user_registration import UserProfile
from .models import BasicCompany, CompanyInfo, Socials, OrgDetails, ProjectHistory, CurrentWork, CompletedWork, \
    Insurance, Safety, Finance, Supplier, Legal, ShippingReceivings
from .serializers import BasicCompanySerializer, CompanyInfoSerializer, SocialsSerializer, OrgDetailsSerializer, \
    ProjectHistorySerializer, CurrentWorkSerializer, CompletedWorkSerializer, InsuranceSerializer, SafetySerializer, \
    SupplierSerializer, FinanceSerializer, LegalSerializer, ShippingReceivingsSerializer
from ..mortgage_calculator.models import PricingModel


class BasicCompanyDetailsCreateView(generics.CreateAPIView):
    serializer_class = BasicCompanySerializer

    def post(self, request, *args, **kwargs):
        userId = request.data.get('userId')
        try:
            UserProfile.objects.get(id=userId)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        company_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in company_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        company_data['filled_fields'] = count

        try:
            basic_company_details = BasicCompany.objects.get(user_id=userId)
            serializer = self.get_serializer(basic_company_details, data=company_data)
        except BasicCompany.DoesNotExist:
            serializer = self.get_serializer(data=company_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=userId)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        userId = request.query_params.get('userId')
        try:
            basic_company_details = BasicCompany.objects.get(user_id=userId)
            serializer = self.get_serializer(basic_company_details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BasicCompany.DoesNotExist:
            return Response({'error': 'Company details not found for the specified userId.'},
                            status=status.HTTP_200_OK)


class CompanyInfoCreateView(generics.CreateAPIView):
    serializer_class = CompanyInfoSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        company_data = request.data
        company_data._mutable = True
        #Create a copy of the request data
        certificate_insurance = request.FILES.get('certificate_insurance')
        certificate_insurance_url = company_data.pop('certificate_insurance_url')
        w9 = request.FILES.get('w9')
        w9_url = company_data.pop('w9_url')

        if certificate_insurance is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(certificate_insurance,
                                                               public_id=certificate_insurance.name)
                company_data['certificate_insurance'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload certificate_insurance to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif certificate_insurance_url[0] != 'null' and certificate_insurance_url[0] != 'undefined':
            company_data['certificate_insurance'] = certificate_insurance_url[0]

        if w9 is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(w9, public_id=w9.name)
                company_data['w9'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload w9 to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif w9_url[0] != 'null' and w9_url[0] != 'undefined':
            company_data['w9'] = w9_url[0]

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in company_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        company_data['filled_fields'] = count

        try:
            company_info = CompanyInfo.objects.get(user_id=user_id)
            serializer = self.get_serializer(company_info, data=company_data)
        except CompanyInfo.DoesNotExist:
            serializer = self.get_serializer(data=company_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            company_info = CompanyInfo.objects.get(user_id=user_id)
            serializer = self.get_serializer(company_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanyInfo.DoesNotExist:
            return Response({'error': 'Company details not found for the specified userId.'},
                            status=status.HTTP_200_OK)


class ProjectTypesView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        templates = PricingModel.objects.values_list('project_type', flat=True)
        return Response(list(templates), status=status.HTTP_200_OK)


class SocialsCreateView(generics.CreateAPIView):
    serializer_class = SocialsSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        socials_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in socials_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        socials_data['filled_fields'] = count

        try:
            socials = Socials.objects.get(user_id=user_id)
            serializer = self.get_serializer(socials, data=socials_data)
        except Socials.DoesNotExist:
            serializer = self.get_serializer(data=socials_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            socials = Socials.objects.get(user_id=user_id)
            serializer = self.get_serializer(socials)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Socials.DoesNotExist:
            return Response({'error': 'Socials not found for the specified user.'},
                            status=status.HTTP_200_OK)


class OrgDetailsCreateView(generics.CreateAPIView):
    serializer_class = OrgDetailsSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        org_details_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in org_details_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                print(key, value)
                count += 1
        org_details_data['filled_fields'] = count

        try:
            org_details = OrgDetails.objects.get(user_id=user_id)
            serializer = self.get_serializer(org_details, data=org_details_data)
        except OrgDetails.DoesNotExist:
            serializer = self.get_serializer(data=org_details_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            org_details = OrgDetails.objects.get(user_id=user_id)
            serializer = self.get_serializer(org_details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrgDetails.DoesNotExist:
            return Response({'error': 'Organization details not found for the specified user.'},
                            status=status.HTTP_200_OK)


class ProjectHistoryCreateView(generics.CreateAPIView):
    serializer_class = ProjectHistorySerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        project_history_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in project_history_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        project_history_data['filled_fields'] = count

        try:
            project_history = ProjectHistory.objects.get(user_id=user_id)
            serializer = self.get_serializer(project_history, data=project_history_data)
        except ProjectHistory.DoesNotExist:
            serializer = self.get_serializer(data=project_history_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            project_history = ProjectHistory.objects.get(user_id=user_id)
            serializer = self.get_serializer(project_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProjectHistory.DoesNotExist:
            return Response({'error': 'Project history not found for the specified user.'},
                            status=status.HTTP_200_OK)


class CurrentWorkCreateView(generics.CreateAPIView):
    serializer_class = CurrentWorkSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        current_work_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in current_work_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        current_work_data['filled_fields'] = count

        try:
            current_work = CurrentWork.objects.get(user_id=user_id)
            serializer = self.get_serializer(current_work, data=current_work_data)
        except CurrentWork.DoesNotExist:
            serializer = self.get_serializer(data=current_work_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            current_work = CurrentWork.objects.get(user_id=user_id)
            serializer = self.get_serializer(current_work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CurrentWork.DoesNotExist:
            return Response({'error': 'Current work not found for the specified user.'},
                            status=status.HTTP_200_OK)


class CompletedWorkCreateView(generics.CreateAPIView):
    serializer_class = CompletedWorkSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        completed_work_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in completed_work_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        completed_work_data['filled_fields'] = count

        try:
            completed_work = CompletedWork.objects.get(user_id=user_id)
            serializer = self.get_serializer(completed_work, data=completed_work_data)
        except CompletedWork.DoesNotExist:
            serializer = self.get_serializer(data=completed_work_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            completed_work = CompletedWork.objects.get(user_id=user_id)
            serializer = self.get_serializer(completed_work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompletedWork.DoesNotExist:
            return Response({'error': 'Completed work not found for the specified user.'},
                            status=status.HTTP_200_OK)


class InsuranceCreateView(generics.CreateAPIView):
    serializer_class = InsuranceSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        insurance_data = request.data.copy()  # Create a copy of the request data
        emr_letter = request.FILES.get('emr_letter')
        emr_letter_url = insurance_data.pop('emr_letter_url')
        bonding_company_letter = request.FILES.get('bonding_company_letter')
        bonding_company_letter_url = insurance_data.pop('bonding_company_letter_url')

        if emr_letter is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(emr_letter,
                                                               public_id=emr_letter.name)
                insurance_data['emr_letter'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload emr letter to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif emr_letter_url[0] != 'null' and emr_letter_url[0] != 'undefined':
            insurance_data['certificate_insurance'] = emr_letter_url[0]

        if bonding_company_letter is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(bonding_company_letter, public_id=bonding_company_letter.name)
                insurance_data['bonding_company_letter'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload bonding company letter to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif bonding_company_letter_url[0] != 'null' and bonding_company_letter_url[0] != 'undefined':
            insurance_data['bonding_company_letter'] = bonding_company_letter_url[0]

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in insurance_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        insurance_data['filled_fields'] = count

        try:
            insurance = Insurance.objects.get(user_id=user_id)
            serializer = self.get_serializer(insurance, data=insurance_data)
        except Insurance.DoesNotExist:
            serializer = self.get_serializer(data=insurance_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            insurance = Insurance.objects.get(user_id=user_id)
            serializer = self.get_serializer(insurance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Insurance.DoesNotExist:
            return Response({'error': 'Insurance not found for the specified user.'},
                            status=status.HTTP_200_OK)


class SafetyCreateView(generics.CreateAPIView):
    serializer_class = SafetySerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        safety_data = request.data.copy()  # Create a copy of the request data
        osha_logs = request.FILES.get('osha_logs')
        osha_logs_url = safety_data.pop('osha_logs_url')
        safety_manual = request.FILES.get('safety_manual')
        safety_manual_url = safety_data.pop('safety_manual_url')

        if osha_logs is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(osha_logs, public_id=osha_logs.name)
                safety_data['osha_logs'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload certificate_insurance to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif osha_logs_url[0] != 'null' and osha_logs_url[0] != 'undefined':
            safety_data['osha_logs'] = osha_logs_url[0]

        if safety_manual is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(safety_manual, public_id=safety_manual.name)
                safety_data['safety_manual'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload w9 to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif safety_manual_url[0] != 'null' and safety_manual_url[0] != 'undefined':
            safety_data['safety_manual'] = safety_manual_url[0]

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in safety_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        safety_data['filled_fields'] = count

        try:
            safety = Safety.objects.get(user_id=user_id)
            serializer = self.get_serializer(safety, data=safety_data)
        except Safety.DoesNotExist:
            serializer = self.get_serializer(data=safety_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            safety = Safety.objects.get(user_id=user_id)
            serializer = self.get_serializer(safety)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Safety.DoesNotExist:
            return Response({'error': 'Safety not found for the specified user.'},
                            status=status.HTTP_200_OK)


class FinanceCreateView(generics.CreateAPIView):
    serializer_class = FinanceSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        finance_data = request.data.copy()  # Create a copy of the request data
        financials_last_year = request.FILES.get('financials_last_year')
        financials_last_year_url = finance_data.pop('financials_last_year_url')

        if financials_last_year is not None:
            try:
                cloudinary_upload = cloudinary.uploader.upload(financials_last_year,
                                                               public_id=financials_last_year.name)
                finance_data['financials_last_year'] = cloudinary_upload['secure_url']
            except:
                return Response({'error': 'Failed to upload certificate_insurance to Cloudinary'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif financials_last_year_url[0] != 'null' and financials_last_year_url[0] != 'undefined':
            finance_data['financials_last_year'] = financials_last_year_url[0]

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in finance_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        finance_data['filled_fields'] = count

        try:
            finance = Finance.objects.get(user_id=user_id)
            serializer = self.get_serializer(finance, data=finance_data)
        except Finance.DoesNotExist:
            serializer = self.get_serializer(data=finance_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            finance = Finance.objects.get(user_id=user_id)
            serializer = self.get_serializer(finance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Finance.DoesNotExist:
            return Response({'error': 'Finance not found for the specified user.'},
                            status=status.HTTP_200_OK)


class SupplierCreateView(generics.CreateAPIView):
    serializer_class = SupplierSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        print(user_id)
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        supplier_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in supplier_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        supplier_data['filled_fields'] = count

        try:
            supplier = Supplier.objects.get(user_id=user_id)
            print(supplier)
            serializer = self.get_serializer(supplier, data=supplier_data)
        except Supplier.DoesNotExist:
            serializer = self.get_serializer(data=supplier_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            supplier = Supplier.objects.get(user_id=user_id)
            serializer = self.get_serializer(supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Supplier.DoesNotExist:
            return Response({'error': 'Supplier not found for the specified user.'},
                            status=status.HTTP_200_OK)


class LegalCreateView(generics.CreateAPIView):
    serializer_class = LegalSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        legal_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in legal_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        legal_data['filled_fields'] = count

        try:
            legal = Legal.objects.get(user_id=user_id)
            serializer = self.get_serializer(legal, data=legal_data)
        except Legal.DoesNotExist:
            serializer = self.get_serializer(data=legal_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            legal = Legal.objects.get(user_id=user_id)
            serializer = self.get_serializer(legal)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Legal.DoesNotExist:
            return Response({'error': 'Legal not found for the specified user.'},
                            status=status.HTTP_200_OK)


class ShippingReceivingsCreateView(generics.CreateAPIView):
    serializer_class = ShippingReceivingsSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        shipping_receivings_data = request.data.copy()  # Create a copy of the request data

        count = 0
        # Iterate through the dictionary and count fields with values
        for key, value in shipping_receivings_data.items():
            if value and key != 'userId' and key != 'id' and key != 'filled_fields':  # This condition checks if the value is not empty or False
                count += 1
        shipping_receivings_data['filled_fields'] = count

        try:
            shipping_receivings = ShippingReceivings.objects.get(user_id=user_id)
            serializer = self.get_serializer(shipping_receivings, data=shipping_receivings_data)
        except ShippingReceivings.DoesNotExist:
            serializer = self.get_serializer(data=shipping_receivings_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            shipping_receivings = ShippingReceivings.objects.get(user_id=user_id)
            serializer = self.get_serializer(shipping_receivings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ShippingReceivings.DoesNotExist:
            return Response({'error': 'Shipping and Receivings not found for the specified user.'},
                            status=status.HTTP_200_OK)


class UpdateCountView(views.APIView):
    def get(self, request, *args, **kwargs):
        # get the user id from the request data
        user_id = request.query_params.get('userId')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # check if the user object exists for the user id
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            # if the user object does not exist, return an error message
            return Response({"error": f"user not found for user_id {user_id}"}, status=status.HTTP_404_NOT_FOUND)

        # create a list of all the models
        models = [BasicCompany, CompanyInfo, Socials, ProjectHistory, CompletedWork, CurrentWork, OrgDetails,
                  Insurance, Safety, Finance, Supplier, Legal, ShippingReceivings]

        # Initialize variables for total fields and filled fields
        total_fields = 0
        filled_fields = 0
        model_names = []

        # Loop through the models
        for model in models:
            # Get the fields for the model
            model_fields = model._meta.get_fields()

            # Calculate total fields in the model
            total_fields += len(model_fields)

            # Try to get the object for the user id
            try:
                obj = model.objects.get(user_id=user_id)
                # If the object exists, increase filled fields by counting non-null fields
                current_filled_fields = obj.filled_fields
                filled_fields += current_filled_fields
                if current_filled_fields > 0:
                    model_names.append(model.__name__)
            except model.DoesNotExist:
                continue

        # Calculate the percentage of fields filled
        if total_fields > 0:
            percentage_filled = (filled_fields / total_fields) * 100
        else:
            percentage_filled = 0.0

        return Response({"count": round(percentage_filled, 2), "models": model_names}, status=status.HTTP_200_OK)
