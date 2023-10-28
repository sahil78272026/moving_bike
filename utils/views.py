from django.http import JsonResponse

from datetime import datetime

def error_404(request,exception):
    response=JsonResponse(data={
        'is_authenticated': False,
        'messages': "end was not found",
        'status_code':404,
        'result': {},
        'additional_data': {}, 
       
        }) 
    response.status_code=404
    return response

def error_403(request,exception):
    response=JsonResponse(data={
        'is_authenticated': False,
        'messages': "something went wong",
        'status_code':403,
        'result': {},
        'additional_data': {}, 
       
        }) 
    response.status_code=403
    return response

def error_500(request):
    response=JsonResponse(data={
        'is_authenticated': False,
        'messages':"server error",
        'status_code':500,
        'result': {},
        'additional_data': {}, 
       
        }) 
    response.status_code=500
    return response

def post_meridiem_time(time):
    if time is not None:
        data_time= time.strftime('%d/%m/%Y,%I:%M %p')
    else:
        data_time=''
    return data_time
        
def post_time(time):
    if time is not None:
        data_time= time.strftime('%d/%m/%Y ,%I:%M %p')
    else:
        data_time=datetime.now().strftime('%d/%m/%Y,%I:%M %p')
    return data_time


def post_meridiem_date(time):
    if time is not None:
        data_time= time.strftime('%d/%m/%Y, %H:%M:%S ,%I:%M %p')
    else:
        data_time=datetime.now().strftime('%d/%m/%Y, %H:%M:%S ,%I:%M %p')
    return data_time



def post_24_date_time(time):
    if time is not None:
        data_time= time.strftime('%d/%m/%Y,%H:%M:%S')
    else:
        data_time=datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    return data_time