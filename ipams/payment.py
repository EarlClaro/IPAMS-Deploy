from django.shortcuts import render
from django.http import JsonResponse
import requests
import base64
from django.db import models
from records.models import SubscriptionPlan



def create_payment_link(request):
    paymongo_api_key = 'sk_test_PUL9xuAM8Sm9GLh3FGura1vr'

    try:
        amount = 0
        description = ''
        if request.GET.get('tier') == 'free':
            amount = 0
            description = 'Free Tier Subscription'
        elif request.GET.get('tier') == 'premium':
            amount = 7900  # Amount in cents (79 PHP)
            description = 'Premium Tier Subscription'
        elif request.GET.get('tier') == 'advanced':
            amount = 14900  # Amount in cents (149 PHP)
            description = 'Advanced Tier Subscription'
        else:
            return JsonResponse({'error': 'Invalid subscription tier'}, status=400)

        data = {
            'data': {
                'attributes': {
                    'amount': amount,
                    'description': description,
                    'remarks': 'Subscription Payment'
                }
            }
        }

        headers = {
            'Authorization': 'Basic ' + base64.b64encode(paymongo_api_key.encode()).decode(),
            'Content-Type': 'application/json'
        }

        response = requests.post('https://api.paymongo.com/v1/links', json=data, headers=headers)
        response_data = response.json()

        checkout_url = response_data['data']['attributes']['checkout_url']

        return JsonResponse({'checkout_url': checkout_url}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
