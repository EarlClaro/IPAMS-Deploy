import requests
from django.http import JsonResponse

def create_payment_link(request):
    paymongo_api_key = 'sk_test_PUL9xuAM8Sm9GLh3FGura1vr'  # Replace this with your actual Paymongo API key

    try:
        data = {
            'data': {
                'attributes': {
                    'amount': 100000,  # Example amount (in cents)
                    'description': 'Tuition',
                    'remarks': 'Extra'
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
