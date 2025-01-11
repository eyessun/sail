# utils/middleware.py
import logging
logger = logging.getLogger(__name__)
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.http import JsonResponse
from django.urls import resolve
import json

# 导入 error_response 以保持响应格式一致
from .response import error_response

# 定义不需要进行 Token 验证的 URL
EXEMPT_URLS = [
    '/api/users/login/admin/',
    '/api/users/login/staff/',
]

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        if path in EXEMPT_URLS:
            return None  # 不验证 Token

        auth = JWTAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, request.auth = user_auth_tuple
        except InvalidToken:
            # 使用 error_response 格式化错误响应
            logger.error("Invalid Token: %s", request.headers.get('Authorization'))
            response = error_response(message='无效的Token', code=1003)
            return JsonResponse(response.data, status=response.status_code)
        except AuthenticationFailed as e:
            logger.error("Invalid Token: %s", request.headers.get('Authorization'))
            logger.error("Authentication Failed: %s", str(e))
            logger.error("Authentication Failed: %s", str(e))
            response = error_response(message='认证失败', code=1004)
            return JsonResponse(response.data, status=response.status_code)
        return None
