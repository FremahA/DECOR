from rest_framework.exceptions import APIException


class UserCategoryNotFound(APIException):
    status_code = 404
    deafult_detail = "The requested user categories do not exist"