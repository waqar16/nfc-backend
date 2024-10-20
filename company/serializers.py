from rest_framework import serializers
from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    display_email = serializers.EmailField(required=False, allow_null=True)

    class Meta:
        model = Company
        fields = "__all__"
