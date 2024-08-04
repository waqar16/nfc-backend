from .serializers import CardSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Card
from django.contrib.auth import get_user_model
from company.models import Company
from company.serializers import CompanySerializer

User = get_user_model()


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def card_list(request):
#     user = request.user
#     cards = Card.objects.filter(user=user)
#     serializer = CardSerializer(cards, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_employee_nfc_cards(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    
    total_cards = Card.objects.filter(employee__company=company).count()
    
    data = {
        'company': CompanySerializer(company).data,
        'total_nfc_cards': total_cards,
    }
    return Response(data, status=status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_card(request):
    user = request.user
    data = request.data
    data['user'] = user.id
    serializer = CardSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_detail(request):
    user = request.user
    try:
        card = Card.objects.get(user=user)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CardSerializer(card)
    return Response(serializer.data)
