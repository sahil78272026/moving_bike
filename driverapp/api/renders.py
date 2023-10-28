from rest_framework import renderers,status
import json

class UserRenderer(renderers.JSONRenderer):
  charset='utf-8'
  def render(self, data, accepted_media_type=None, renderer_context=None):
    response = ''
    if 'ErrorDetail' in str(data):
        response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_403_FORBIDDEN,
            'messages':" Token is invalid or expired",
            'result': data,
            'additional_data': {},
            }   
        response = json.dumps(response_payload)
        
    # elif '401' in str(data):
    #     response_payload = {
    #         'is_authenticated': False,
    #         'status': status.HTTP_401_UNAUTHORIZED,
    #         'messages':" Token is invalid or expired",
    #         'result': data,
    #         'additional_data': {},
    #         }   
    #     response = json.dumps(response_payload)
    else:
      response = json.dumps(data)
    
    return response

class UserTokenRenderer(renderers.JSONRenderer):
  charset='utf-8'
  def render(self, data, accepted_media_type=None, renderer_context=None):
    response = ''
    if 'ErrorDetail' in str(data):
        response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_401_UNAUTHORIZED,
            'messages':"Authentication credentials were not provided",
            'result': data,
            'additional_data': {},
            }   
        response = json.dumps(response_payload)
    else:
      response = json.dumps(data)
    
    return response
