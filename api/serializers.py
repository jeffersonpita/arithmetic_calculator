from rest_framework import serializers
from api.models import Operation, Record


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'type', 'type_str', 'cost']

class RecordSerializer(serializers.ModelSerializer):
    operation_type_str = serializers.CharField(source='operation.type_str')

    class Meta:
        model = Record
        fields = ['id', 'date', 'operation', 'cost', 'operation_type_str']

        