from django.contrib.auth import authenticate
from users.models import User
from rest_framework.exceptions import AuthenticationFailed
import environ 


env = environ.Env()
EXTERNAL_PASSWORD = env("EXTERNAL_PASSWORD")

def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            
            registered_user = authenticate(
                email=email, password=EXTERNAL_PASSWORD)

            return {
                'full_name' : registered_user.full_name,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {'email': email, 'full_name': name, 'password': EXTERNAL_PASSWORD}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=EXTERNAL_PASSWORD)
        return {
            'email': new_user.email,
            'full_name': new_user.full_name,
            'tokens': new_user.tokens()
        }
