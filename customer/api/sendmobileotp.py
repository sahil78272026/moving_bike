import random,requests

def send_otp(mobile,country_code):
    url = "https://api.authkey.io/request"
    otp="".join([str(random.randint(0,9)) for i in range(4)])
    querystring={
        "authkey":"631d38ba78dd302e",
        "country_code":f"{country_code}",
        "mobile":f"{mobile}",
        "sid":"7965",
        "otp":f"{otp}"
        }
    response_data = requests.request("GET", url, params=querystring)
    response={
        "otp":f"{otp}",
        "messages":response_data.text
    }
    return response
def custom_send_otp(mobile,country_code,pwd):
    url = "https://api.authkey.io/request"
    # otp="".join([str(random.randint(0,9)) for i in range(4)])
    otp=pwd
    querystring={
        "authkey":"631d38ba78dd302e",
        "country_code":f"{country_code}",
        "mobile":f"{mobile}",
        "sid":"7965",
        "otp":f"{otp}"
        }
    response_data = requests.request("GET", url, params=querystring)
    response={
        "otp":f"{otp}",
        "messages":response_data.text
    }
    return response