from rest_framework import serializers
from .models import Company, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = Company
        fields = "__all__"
