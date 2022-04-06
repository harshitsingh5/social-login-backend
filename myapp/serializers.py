from rest_framework import serializers
from .auth import *
import os
from rest_framework.exceptions import AuthenticationFailed


GOOGLE_CLIENT_ID='41857448079-of9kcsc6q9bo6ucrcfodr96mcr9hnp0o.apps.googleusercontent.com'


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)
        # print(user_data)
        try: 
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except:
            raise serializers.ValidationError('The token is invalid.')


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        # print(user_data)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('ve: The token is invalid or expired. Please login again.')

        # if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        if user_data['aud'] != GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)

class LinkedinSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        return register_social_user(
                provider='provider',
                user_id='user_id',
                email='email',
                name='name'
            )