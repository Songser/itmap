# coding=utf-8

errors = {
    'NoAuthorizationError': {
        'message': "No Authorization",
        'status': 401,
    },
    'InvalidSignatureError': {
        'message': "Signature verification failed",
        'status': 401,
    },
    'InvalidHeaderError': {
        'message': "Invalid Header",
        'status': 422,
    },
    'RevokedTokenError': {
        'message': "Token has been revoked",
        'status': 401,
    },
    'FreshTokenRequired': {
        'message': "Fresh token required",
        'status': 401,
    },
    'ExpiredSignatureError': {
        'message': "Signature has expired",
        'status': 401,
    },

}
