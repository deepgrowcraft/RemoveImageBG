# import logging

# from django.conf import settings
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
# from rest_framework.permissions import IsAuthenticated

# from .settings import WW_PLATFORM_SECRET_ENV_VAR


# class WWClientSecretView(TokenAuthentication):
#     CLIENT_KEY_HEADER_NAME = "CLIENT-KEY"
#     CLIENT_SECRET_HEADER_NAME = "CLIENT-SECRET"

#     def authenticate(self, request):
#         if (request.headers.get(self.CLIENT_KEY_HEADER_NAME) is None) or (
#             request.headers.get(self.CLIENT_SECRET_HEADER_NAME) is None
#         ):
#             logging.info("[SECURITY] The request doesn't have the header token")
#             raise AuthenticationFailed(
#                 {
#                     "success": False,
#                     "message": "You need to be authenticated to access this resource",
#                     "code": 401,
#                 }
#             )
#         if (
#             request.headers.get(self.CLIENT_KEY_HEADER_NAME)
#             != WW_PLATFORM_SECRET_ENV_VAR["WWS_WW_PLATFORM_SECRET"]
#         ):
#             logging.info("[SECURITY] Invalid CLIENT-KEY.")
#             raise AuthenticationFailed(
#                 {
#                     "success": False,
#                     "message": "Invalid CLIENT-KEY.",
#                     "code": 401,
#                 }
#             )
#         if (
#             request.headers.get(self.CLIENT_SECRET_HEADER_NAME)
#             != settings.WW_PLATFORM_SECRET_VAR_KEY["WWS_WW_PLATFORM_SECRET"]
#         ):
#             logging.info(
#                 "[SECURITY] The CLIENT SECRET received and the CLIENT SECRET configured do not match"
#             )
#             raise AuthenticationFailed(
#                 {
#                     "success": False,
#                     "message": "The CLIENT SECRET received and the CLIENT SECRET configured do not match",
#                     "code": 401,
#                 }
#             )
#         return self.authenticate_credentials(
#             request.headers.get(self.CLIENT_SECRET_HEADER_NAME)
#         )

#     def authenticate_credentials(self, key):
#         return {}, key


import logging
from functools import wraps

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .settings import WW_PLATFORM_SECRET_ENV_VAR


def require_client_secret(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check for CLIENT-KEY and CLIENT-SECRET headers
        client_key = request.headers.get("CLIENT-KEY")
        client_secret = request.headers.get("CLIENT-SECRET")

        if not client_key or not client_secret:
            logging.info("[SECURITY] The request doesn't have the necessary headers")
            return Response(
                {
                    "success": False,
                    "message": "You need to be authenticated to access this resource",
                    "code": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if client_key != WW_PLATFORM_SECRET_ENV_VAR.get("WWS_WW_PLATFORM_SECRET"):
            logging.info("[SECURITY] Invalid CLIENT-KEY.")
            return Response(
                {
                    "success": False,
                    "message": "Invalid CLIENT-KEY.",
                    "code": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if client_secret != settings.WW_PLATFORM_SECRET_VAR_KEY.get(
            "WWS_WW_PLATFORM_SECRET"
        ):
            logging.info("[SECURITY] CLIENT SECRET mismatch.")
            return Response(
                {
                    "success": False,
                    "message": "The CLIENT SECRET received and the CLIENT SECRET configured do not match.",
                    "code": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # If the headers are correct, proceed with the view
        return view_func(request, *args, **kwargs)

    return _wrapped_view
