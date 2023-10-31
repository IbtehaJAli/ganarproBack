from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from ..models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        """Method for setting up user"""
        self.signup_url = api_reverse("authentication:user-registration")

        self.valid_user = {
            "email": "test@example.com",
            "username": "test",
            "password": "Pass@123",
        }

        self.invalid_user_with_missing_fields = {
            "email": "test@example.com",
            "password": "Pass@123",
        }

        self.invalid_user_with_empty_fields = {
            "email": "",
            "username": "username",
            "password": "Pass@123",
        }
        self.invalid_user_with_invalid_fields = {
            "email": "",
        }

    def signup_user(self):
        """Signup user successfully"""
        response = self.client.post(self.signup_url, self.valid_user, format="json")

        return response

    def signup_user_with_invalid_details(self, payload):
        """Signup user with missing fields"""
        response = self.client.post(
            self.signup_url, payload, format="json"
        )
        return response
