from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global API exception handler.
    """

    response = exception_handler(
        exc,
        context,
    )

    if response is not None:

        response.data = {
            "success": False,
            "status_code": response.status_code,
            "message": get_error_message(
                response.data
            ),
            "errors": response.data,
        }

    return response


def get_error_message(data):

    if isinstance(data, dict):

        if "detail" in data:
            return data["detail"]

        return "Validation error."

    return "Something went wrong."