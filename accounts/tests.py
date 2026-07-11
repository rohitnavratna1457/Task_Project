from django.test import TestCase

# Create your tests here.
# test.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, Calculation


class UserAPITestCase(APITestCase):

    def setUp(self):
        """
        This method runs before every test case.
        We create a test user here.
        """
        self.register_url = reverse('register')   # URL name from urls.py
        self.login_url = reverse('login')

        self.user_data = {
            "email": "test@example.com",
            "password": "123456"
        }

        # Create user manually in DB
        self.user = User.objects.create(**self.user_data)

    # ✅ TEST REGISTER API (POST)
    def test_register_user(self):
        new_user_data = {
            "email": "new@example.com",
            "password": "123456"
        }

        response = self.client.post(self.register_url, new_user_data, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check DB entry
        self.assertEqual(User.objects.count(), 2)

    # ✅ TEST REGISTER API (GET with pagination)
    def test_get_users(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination keys
        self.assertIn('results', response.data)

    # ✅ TEST LOGIN SUCCESS
    def test_login_success(self):
        response = self.client.post(self.login_url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)

    # ❌ TEST LOGIN FAILURE
    def test_login_failure(self):
        wrong_data = {
            "email": "test@example.com",
            "password": "wrongpass"
        }

        response = self.client.post(self.login_url, wrong_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CalculationAPITestCase(APITestCase):

    def setUp(self):
        """
        Setup user and URLs
        """
        self.calculate_url = reverse('calculate')
        self.history_url = reverse('history')

        self.user = User.objects.create(
            email="test@example.com",
            password="123456"
        )

        self.valid_data = {
            "dob": "1995-05-10",
            "amount": 1000,
            "years": 5
        }

    # ✅ TEST CALCULATION API (POST)
    def test_calculation_success(self):
        response = self.client.post(self.calculate_url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

        # Check DB entry created
        self.assertEqual(Calculation.objects.count(), 1)

    # ❌ TEST CALCULATION INVALID DATA
    def test_calculation_invalid(self):
        invalid_data = {
            "dob": "",   # Invalid
            "amount": 1000
        }

        response = self.client.post(self.calculate_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ✅ TEST GET CALCULATIONS (PAGINATION)
    def test_get_calculations(self):
        # Create sample records
        for _ in range(6):
            Calculation.objects.create(
                user=self.user,
                input_data={"test": "data"},
                output_data={"result": "ok"}
            )

        response = self.client.get(self.calculate_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    # ✅ TEST HISTORY API
    def test_history_api(self):
        Calculation.objects.create(
            user=self.user,
            input_data={"a": 1},
            output_data={"b": 2}
        )

        response = self.client.get(self.history_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
