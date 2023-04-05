from django.test import SimpleTestCase, TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.models import User

class JWTTests(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.email = "admin@admin.com"
        self.data = {
            'username': self.username,
            'password': self.password
        }

        # create user
        user = User.objects.create_user(username=self.username, 
                                        password=self.password, 
                                        email=self.email)

        # assert the user is saved in db
        self.assertEqual(User.objects.count(), 1)

    def test_jwt_token_creation(self):
        """
        Tests the token creation
        """
        # post to get token 
        response = self.client.post(reverse('token_obtain_pair'), self.data, format='json')

        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure that the tokens are returned
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])
        

    def test_jwt_token_refresh(self):
        """
        Tests the token refresh feature
        """
        # post to get token 
        token_obtain_response = self.client.post(reverse('token_obtain_pair'), self.data, format='json')
        refresh_token = token_obtain_response.data['refresh']
        access_token = token_obtain_response.data['refresh']

        # post to refresh the first token 
        token_refresh_response = self.client.post(reverse('token_refresh'), {'refresh':refresh_token}, format='json')

         # assert the response is OK
        self.assertEqual(token_refresh_response.status_code, status.HTTP_200_OK)
        
        # make sure that the tokens are returned
        self.assertIsNotNone(token_refresh_response.data['access'])
        self.assertIsNotNone(token_refresh_response.data['refresh'])

        # assert the old and new tokens are different
        self.assertNotEqual(token_refresh_response.data['access'], access_token)
        self.assertNotEqual(token_refresh_response.data['refresh'], refresh_token)

