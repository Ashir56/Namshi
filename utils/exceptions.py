from rest_framework.exceptions import ValidationError, AuthenticationFailed, \
    NotAuthenticated, NotFound
from rest_framework.views import exception_handler
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings
from Buyer.serializer import BuyerSerializer


def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_codes(value) for key, value in detail.items()}
    return detail.code


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    # Update the structure of the response data.
    customized_response = []
    if isinstance(exc, ValidationError):

        if response is not None:
            response.status_code = 500
        codes = _get_codes(response.data)
        code = ''
        for key, value in codes.items():
            code = str(value)
        print(response.data)
        if 'does_not_exist' in code:
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            key = list(response.data.keys())[0]
            response_dict = {
                "success": False,
                key: "Object Does Not Exist"
            }
            response.data = response_dict

        elif 'required' in code:
            print(response.data.keys())
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            key = list(response.data.keys())[0]
            response_dict = {
                "success": False,
                key: customized_response[0][0]
            }
            response.data = response_dict

        elif 'incorrect_type' in code:

            print(response.data.keys())
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            key = list(response.data.keys())[0]
            response_dict = {
                "success": False,
                key: customized_response[0][0]
            }
            response.data = response_dict

        elif 'invalid' in code:

            print(response.data.keys())
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            key = list(response.data.keys())[0]
            response_dict = {
                "success": False,
                key: customized_response[0][0]
            }
            response.data = response_dict

        elif 'blank' in code:
            print(response.data.keys())
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            response_dict = {
                "success": False,
                list(response.data.keys())[0]: customized_response[0][0]
            }
            response.data = response_dict

        elif 'unique' in code:
            print(response.data.keys())
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            response_dict = {
                "success": False,
                list(response.data.keys())[0]: customized_response[0][0]
            }
            response.data = response_dict

        else:
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            response_dict = {
                "success": False,
                "message": "Something went wrong"
            }
            response.data = response_dict

    if isinstance(exc, AuthenticationFailed):

        response_dict = {}
        if response is not None:
            response.status_code = 401
            response_dict = {
                "success": False,
                "message": "You do not have permission for following tasks"
            }
        response.data = response_dict
    if isinstance(exc, NotAuthenticated):
        response_dict = {}
        if response is not None:
            response.status_code = 401
            response_dict = {
                "success": False,
                "message": "Authentication Credentials were not Provided"
            }
        response.data = response_dict

    if isinstance(exc, NotFound):
        response_dict = {}
        if response is not None:
            response.status_code = 404
            response_dict = {
                "success": False,
                "message": "Object Does Not Exist"
            }
        response.data = response_dict

    return response


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': str(user.pk),
        'email': user.email,
        'username': user.username,
        'is_superuser': user.is_superuser,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }
