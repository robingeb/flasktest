


#Funktioniert noch nicht!!!!
import requests

api_login = '*'
api_password = "03e4cc87-fadd-4ada-9ca5-9656d0247107"
environmentId = "gebhardt"
base_url = "https://" + environmentId + ".weclapp.com/webapp/api/v1/"

def login(base_url,api_login,api_password):
    print("Getting token...")
    data_get = {'username': api_login,
                'password': api_password,
                'loginMode': 1}
    r = requests.post(base_url + 'auth/login', data=data_get)
    if r.ok:
        authToken = r.headers['X-MSTR-AuthToken']
        cookies = dict(r.cookies)
        print("Token: " + authToken)
        return authToken, cookies
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))


login(base_url,api_login,api_password)
