from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class InboundCallView(APIView):
    def post(self, request):
        try:
            # Make request to Vapi
            response = requests.post(
                "https://api.vapi.ai/call",
                json={
                    "phoneNumberId": "8ae7fab6-5e0f-462c-870a-dadd9b6499ae",
                    "phoneCallProviderBypassEnabled": True,
                    "assistantOverrides": {
                        "variableValues": {
                            "name": "John",
                            "location": "India"
                        }
                    },
                    "customer": {
                        "number": request.POST.get('Caller')
                    },
                    "assistantId": "76999a90-c9db-41ad-9bde-ac541e5bdc56"
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer c686707b-e3bb-4b22-90e7-23ff800e23e5"
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            return HttpResponse(
                content=result["phoneCallProviderDetails"]["twiml"],
                content_type="text/plain"
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Vapi API error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
