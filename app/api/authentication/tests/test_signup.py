import json
from sys import breakpointhook

from rest_framework import status

from ...utils.constants import SIGNUP_SUCCESS_MESSAGE
from ...utils.serialization_errors import error_dict
from .base_test import TestBaseCase


class RegistrationTest(TestBaseCase):
    """User signup test cases"""

    def test_user_signup_succeed(self):
        """Test API can successfully register a new user"""
        response = self.client.post(self.signup_url, self.valid_user, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], SIGNUP_SUCCESS_MESSAGE)

    def test_user_signup_with_blank_fields_fails(self):
        """Test register a new user with missing details"""
        response = self.signup_user_with_invalid_details(self.invalid_user_with_missing_fields)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)["errors"][0],
            error_dict["required"].format("Username"),
        )

    def test_user_signup_with_empty_fields_fails(self):
        """Test register a new user with empty fields"""
        response = self.signup_user_with_invalid_details(self.invalid_user_with_empty_fields)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)["errors"][0],
            error_dict["blank"].format("Email"),
        )

    def test_signup_existing_user(self):
        """Test register existing user"""
        self.signup_user()
        response = self.client.post(self.signup_url, self.valid_user, format="json")
        self.assertEqual(
            json.loads(response.content)["errors"][0],
            error_dict["already_exist"].format("Email"),
        )
    

    def test_signup_invalid_fields(self):
        """Test register existing user"""
        response = self.signup_user_with_invalid_details(self.invalid_user_with_invalid_fields)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
