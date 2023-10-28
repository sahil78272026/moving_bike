from ast import In
from re import I
from .models import *
import jwt
from .config import *
from django.http.response import JsonResponse
from rest_framework import status
from functools import wraps

class InvalidTokenError(Exception):

    def __init__(self,message):
        self.message = message
        super().__init__(self.message)


def validate_token(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        raise InvalidTokenError(message="Token missing.")
    token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ","")
    
    if  AccessToken.objects.filter(token = token).exists():
        token_obj = AccessToken.objects.get(token=token)
        access_token = jwt.decode(token,SECRET_KEY_JWT, algorithms='HS256')
        if access_token['type'] != 'access':
            raise InvalidTokenError(message="Invalid access token")
        id=access_token['id']
        user_id  = str(token_obj.user.id)
        if id == user_id:
            return user_id
        else:
            raise InvalidTokenError(message="Invalid access token")
    else:
        raise InvalidTokenError(message="Invalid access token")


        

def login_required(func,*args,**kwargs):
    @wraps(func)
    def inner(*args,**kwargs):
            user_id = validate_token(args[0])
            return func(user_id=user_id,*args,**kwargs)
    return inner