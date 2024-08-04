from .views import create_card, card_detail
from django.urls import path

urlpatterns = [
    path('create_card/', create_card, name='create_card'),
    path('card_detail/', card_detail, name='card_detail')
]