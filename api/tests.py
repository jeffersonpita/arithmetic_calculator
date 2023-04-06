
from django.test import SimpleTestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Operation, Record, User
from api.operations import perform_operation

class BasicOperationTests(SimpleTestCase):
    @parameterized.expand([
        [[1, 1, 1, 1, 2]],
        [[1, 2, 2, 1, 4]],
        [[2, 2, 2, 1, 0]],
        [[2, 3, 2, 1, 1]],
        [[3, 3, 2, 1, 6]],
        [[3, 3, 5, 1, 15]],
        [[4, 3, 2, 1, 1.5]],
        [[4, 4, 2, 1, 2]],
        [[5, 2, 3, 1, 8]],
        [[5, -2, 3, 1, -8]],
        [[7, 0, 0, 0, "Invalid operation"]],
        [[1, None, 1, 0, "Operator 1 and Operator 2 are required"]],
        [[1, "", 1, 0, "Operator 1 and Operator 2 are required"]],
        [[1, "asd", 1, 0, "Invalid operator"]],
    ])
    def test_perform_arithmetic_operation(self, data):
        ''''
        Test the arithmetic operations
        '''
        (operation_type, 
         operator1, 
         operator2, 
         result_status, 
         response_data) = data
        
        result = perform_operation(operation_type=operation_type, 
                                   operator1=operator1, 
                                   operator2=operator2)
        
        self.assertEqual(result['status'], result_status)

        if result['status']==1:
            self.assertEqual(result['response_data'], response_data)
        else:
            self.assertEqual(result['error_message'], response_data)

    def test_perform_random_string_operation(self):
        '''
        Test the random string operation
        '''
        result = perform_operation(operation_type=6)
        
        self.assertEqual(result['status'], 1)
        self.assertIsNotNone(result['response_data'])
        

class AuthenticatedViewTests(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.email = "admin@admin.com"
        self.data = {
            'username': self.username,
            'password': self.password
        }

        # create user
        self.user = User.objects.create_user(username=self.username, 
                                        password=self.password, 
                                        email=self.email)

        # post to get token 
        response = self.client.post(reverse('token_obtain_pair'), self.data, format='json')
        self.token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.token)}


class HomeViewTests(AuthenticatedViewTests):
    def test_home_view(self):
        """
        Tests the home view
        """
        # perform the request to home 
        response = self.client.get(reverse('home'), headers=self.headers, format='json')

         # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure that the right user is logged
        self.assertEqual(response.data['username'], self.username)

        # assert the operations returned
        self.assertEqual(len(response.data['operations']), Operation.objects.count())


class OperationViewTests(AuthenticatedViewTests):
    @parameterized.expand([
        [[1, 1, 1, 1, 2]],
        [[1, 2, 2, 1, 4]],
        [[2, 2, 2, 1, 0]],
        [[2, 3, 2, 1, 1]],
        [[3, 3, 2, 1, 6]],
        [[3, 3, 5, 1, 15]],
        [[4, 3, 2, 1, 1.5]],
        [[4, 4, 2, 1, 2]],
        [[5, 2, 3, 1, 8]],
        [[5, -2, 3, 1, -8]],
        [[1, None, 1, 0, "Operator 1 and Operator 2 are required"]],
        [[1, "", 1, 0, "Operator 1 and Operator 2 are required"]],
        [[1, "asd", 1, 0, "Invalid operator"]],
    ])
    def test_operation_view(self, data):
        """
        Tests the operation view with arithmetic operations
        """
        (operation_type, 
         operator1, 
         operator2, 
         result_status, 
         response_data) = data
        
        operation = Operation.objects.get(type=operation_type)

        # update the user balance so the operation can be performed
        self.user.balance = operation.cost
        self.user.save()

        
        # perform the POST request to operation 
        response = self.client.post(reverse('operation'), 
                                    { 
                                        "operation_id": operation.id,
                                        "operator1": operator1,
                                        "operator2": operator2,
                                     },
                                    headers=self.headers, 
                                    format='json')

         # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.data['status']==1:
            self.assertEqual(response.data['response_data'], response_data)
        else:
            self.assertEqual(response.data['error_message'], response_data)

    def test_operation_view_random_string(self):
        """
        Tests the operation view with random_string operation
        """
        operation = Operation.objects.get(type=6)

        # update the user balance so the operation can be performed
        self.user.balance = operation.cost
        self.user.save()

        
        # perform the POST request to operation 
        response = self.client.post(reverse('operation'), 
                                    { 
                                        "operation_id": operation.id,
                                        "operator1": "",
                                        "operator2": "",
                                     },
                                    headers=self.headers, 
                                    format='json')

         # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['status'], 1)
        self.assertIsNotNone(response.data['response_data'])
        


class LogoutViewTests(AuthenticatedViewTests):
    def test_logout_view(self):
        """
        Tests the logout view
        """
        # perform the request to home 
        response = self.client.get(reverse('home'), headers=self.headers, format='json')
        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # perform the request to logout 
        logout_response = self.client.post(reverse('logout'), 
                                           {'refresh_token':self.refresh_token}, 
                                           headers=self.headers, 
                                           format='json')
        # assert the response is HTTP_205_RESET_CONTENT
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)
        

class RecordsViewTests(AuthenticatedViewTests):
    def test_record_view(self):
        """
        Tests the records view with no records
        """
        # perform the request to records 
        response = self.client.get(reverse('records'), headers=self.headers, format='json')

        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure that the count is equal to 0
        self.assertEqual(response.data['count'], 0)

        # assert the results returned
        self.assertEqual(len(response.data['results']), 0)


    def test_record_view_with_one_record(self):
        """
        Tests the records view with one record
        """
        operation = Operation.objects.get(type=1)
        record = Record(user=self.user, operation=operation, cost=operation.cost, 
                        user_balance=self.user.balance, operation_response="" )
        record.save()

        # perform the request to records 
        response = self.client.get(reverse('records'), headers=self.headers, format='json')

        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure that the count is equal to 1
        self.assertEqual(response.data['count'], 1)

        # assert the results returned
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], record.id)

    def test_record_view_delete(self):
        """
        Tests the record_delete view
        """
        operation = Operation.objects.get(type=1)
        record = Record(user=self.user, operation=operation, cost=operation.cost, 
                        user_balance=self.user.balance, operation_response="" )
        record.save()

        # perform the request to record_delete 
        response = self.client.delete(reverse('record_delete', kwargs={'id': record.id}), 
                                    headers=self.headers, format='json')

        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # make sure that there are no records on the database
        self.assertEqual(Record.objects.filter(is_active=True).count(), 0)

    def test_record_view_filter(self):
        """
        Tests the records view filter
        """
        # create records of all types
        for i in Operation.TYPE_CHOICES:
            operation = Operation.objects.get(type=i[0])
            record = Record(user=self.user, operation=operation, cost=operation.cost, 
                            user_balance=self.user.balance, operation_response="" )
            record.save()

        # perform the request to records 
        response = self.client.get(reverse('records'), headers=self.headers, format='json')

        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # make sure that the count is right
        self.assertEqual(response.data['count'], len(Operation.TYPE_CHOICES))

         # perform the request to records 
        response = self.client.get(reverse('records'), {"operations":1}, 
                                   headers=self.headers, format='json')
        
        # assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

         # make sure that there's only one record for the operation_type 1
        self.assertEqual(response.data['count'], 1)

        

    

        


        