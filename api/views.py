from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from api.models import Operation, Record
from api.operations import dict_message, perform_operation
from api.serializers import OperationSerializer, RecordSerializer



class HomeView(APIView):  
   permission_classes = (IsAuthenticated,)
   def get(self, request):
        # return all operations for now
        operations = Operation.objects.all()
        serializer = OperationSerializer(operations, many=True)
        content = {'username': request.user.username, 
                   'user_balance': request.user.balance,
                   'operations': serializer.data}
        return Response(content)
   

class OperationView(APIView):  
   permission_classes = (IsAuthenticated,)
   def post(self, request):
        # search for the operation based on the received operation_id
        operation_id = request.data["operation_id"]
        try:
            operation = Operation.objects.get(id=operation_id)
        except Exception as e:
            return Response(dict_message(error_message="Invalid operation"))

        user = request.user
        response = dict_message(error_message="Unknown error")

        # perform operation if the user has enough balance
        if user.balance >= operation.cost:
            response = perform_operation(operation_type=operation.type, 
                                         operator1=request.data["operator1"], 
                                         operator2=request.data["operator2"])
            
            # check if the operation is performed sucessfully
            if response['status'] == 1:
                try:
                    # saves the record
                    record = Record(cost=operation.cost, 
                                    user_balance=request.user.balance, 
                                    operation_response=response, 
                                    operation=operation, user=user)
                    record.save()

                    # updates user balance
                    user.balance -= operation.cost
                    user.save()

                    # return updated user_balance
                    response["user_balance"] = user.balance
                    return Response(response)
                except Exception as e:
                    return Response(dict_message(error_message=str(e)))
        else:
            return Response(dict_message(error_message="The user balance is not enough"))
        return Response(response)
   
   

class RecordView(APIView, PageNumberPagination):  
   permission_classes = (IsAuthenticated,)
   page_size = 10
   def get(self, request):
        # return all records related to the logged user
        queryset = Record.objects.filter(user__id=request.user.id, 
                                         is_active=True).order_by('-date')
        if 'operations' in request.GET:
            if int(request.GET['operations']) > 0:
                queryset = queryset.filter(operation__type=int(request.GET['operations']))

        records = self.paginate_queryset(queryset, request, view=self)
        serializer = RecordSerializer(records, many=True)
        return self.get_paginated_response(serializer.data)
   
   def delete(self, request, id=None):
        try:
            record = Record.objects.get(id=id)
            record.is_active = False
            record.save()
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_202_ACCEPTED)
   

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
          

