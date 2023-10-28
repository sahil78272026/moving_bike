from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated,AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        token = response.data.get('access')
        response.data = {
            'access_token': token 
        }
        return response
def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        response_payload = {
            'is_authenticated': False,
            'status': 101,
            'messages': 'Please enter an access token',
            'result': {},
            'additional_data': {},  
        }
        return Response(response_payload)
    elif isinstance(exc, AuthenticationFailed):
        response_payload = {
            'is_authenticated': False,
            'status': 101,
            'messages': 'Your token is expired or invalid',
            'result': {},
            'additional_data': {},  
        }
        return Response(response_payload)
    else:
        pass
    return exception_handler(exc, context)
