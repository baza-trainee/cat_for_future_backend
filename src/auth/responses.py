from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.openapi import OpenAPIResponseType
from fastapi import status

from src.auth.auth_config import auth_backend


logout_responses: OpenAPIResponseType = {
    **{
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
    **auth_backend.transport.get_openapi_logout_responses_success(),
}

login_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Bad credentials or the user is inactive.",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                    },
                    ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                        "summary": "The user is not verified.",
                        "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    **auth_backend.transport.get_openapi_login_responses_success(),
}
is_accessible_resposes: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.VERIFY_USER_BAD_TOKEN: {
                        "summary": "The user is not authorized.",
                        "value": {"detail": "Unauthorized"},
                    },
                }
            }
        },
    },
}
