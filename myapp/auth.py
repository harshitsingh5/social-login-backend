from django.contrib.auth import authenticate, login
from .models import User
from .values import *
import os
import random
from rest_framework.exceptions import AuthenticationFailed
import facebook
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
import requests


class Facebook:
    @staticmethod
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expireddd."

class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, grequests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The token is either invalid or has expired"

class Linkedin:
    @staticmethod
    def validate(code):
        try:
            # print('inside validate')
            data = {
                'grant_type':'authorization_code',
                'code':code,
                'client_id':'78xx67hewmxxlr',
                'client_secret':'X6Ju6nl6q5a9UF05',
                'redirect_uri':'https://localhost:3000/linkedin',
            }
            lnkd_verify_url = 'https://www.linkedin.com/oauth/v2/accessToken'
            r = requests.post(lnkd_verify_url, data=data)
            jsonified = r.json()
            access_token = jsonified['access_token']
            # print(jsonified)
            # return jsonified

            #### fetching the profile data
            ## token_data = '\'TOK:' + access_token + "\'"
            prof_url = 'https://api.linkedin.com/v2/me'
            params = {'oauth2_access_token': access_token}
            prof_data = requests.get(prof_url, params=params)
            ## print(prof_data.json())
            return r.json(), prof_data.json()
        except:
            return "The token is either invalid or has expired"


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user = User.objects.filter(email=email)
    if filtered_user.exists():

        if provider == filtered_user[0].auth_provider:
            registered_user = authenticate(email=email, password=sample_pass)
            # login(filtered_user)
            # registered_user = filtered_user
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}
        else:
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': sample_pass}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=sample_pass)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }

