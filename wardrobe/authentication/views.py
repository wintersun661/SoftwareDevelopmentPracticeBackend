from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from authentication.models import * #User

import json

# Create your views here.

def sign_in(request):
    if request.method == 'POST':
        try:
            body = json.loads(bytes.decode(request.body, encoding='utf-8'))
            print(body)
        except:
            response = {
                'status': '101',
                'message': 'Ill-formed JSON request body'
            }
        else:
            username, password = body.get('username'), body.get('password')
            if username == None:
                response = {
                    'status': '102',
                    'message': 'Missing username',
                }
            else:
                user = User.get_user(username)
                if user == None:
                    response = {
                        'status': '103',
                        'message': 'User does not exist',
                    }
                elif password == None:
                    response = {
                        'status': '104',
                        'message': 'Missing password',
                    }
                elif check_password(password, user.encrypted_password) == False:
                    response = {
                        'status': '105',
                        'message': 'Wrong password',
                    }
                elif 'username' not in request.session:
                    request.session['username'] = username
                    response = {
                        'status': '000',
                        'message': 'Signed in successfully',
                    }
                else:
                    response = {
                        'status': '001',
                        'message': 'Signed in already',
                    }
    else:
        response = {
            'status': '100',
            'message': 'Fail to log in',
        }
    return JsonResponse(response)


def sign_out(request):
    if request.method == 'POST':
        try:
            body = json.loads(bytes.decode(request.body, encoding='utf-8'))
            print(body)
        except:
            response = {
                'status': '101',
                'message': 'Ill-formed JSON request body'
            }
        else:
            username = body.get('username')
            if request.session.get('username') == username:
                del(request.session['username'])
                response = {
                    'status': '000',
                    'message': 'Signed out successfully',
                }
            else:
                response = {
                    'status': '102',
                    'message': 'Not logged in',
                }
    else:
        response = {
            'status': '100',
            'message': 'Fail to log out'
        }
    return JsonResponse(response)