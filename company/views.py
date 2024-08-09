from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer

User = get_user_model()

# Email backend configuration (assuming you're using SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change to your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'wa4752928@gmail.com'  # Change to your email
EMAIL_HOST_PASSWORD = 'xdnr awsy qrhk tqrt'  # Change to your email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def company_profile_list(request):
    if request.method == 'GET':
        profiles = Company.objects.filter(user=request.user)
        serializer = CompanySerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_detail(request, pk):
    try:
        company = Company.objects.get(user=pk)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        # print(serializer.errors)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.filter(company__user=request.user)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            company = Company.objects.filter(user=request.user).first()
            if company:
                employee = serializer.save(company=company)
                registration_url = request.build_absolute_uri(reverse('complete-registration', args=[employee.registration_token, employee.email, employee.first_name, employee.last_name]))
                send_mail(
                    'Complete Your Registration',
                    f'Please complete your registration by visiting the following link: {registration_url}',
                    DEFAULT_FROM_EMAIL,
                    [employee.email],
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "No associated company found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def complete_registration(request, token, email, first_name, last_name):
    try:
        employee = Employee.objects.get(registration_token=token)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def employee_detail(request, email):
    try:
        employee = Employee.objects.get(email=email)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the associated user
        if employee.user:
            employee.user.delete()

        # Delete the employee
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee_profile(request, email):
    try:
        user = User.objects.get(email=email)
        # user = User.objects.all()
        print(user)

        if request.user.profile_type != 'company':
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        employee_profile = Employee.objects.get(email=email)
        user.delete()
        employee_profile.delete()
        
        return Response({'detail': 'Profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response({'detail': 'Employee profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
