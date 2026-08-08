from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Global pagination class.

    Example:
    /api/employees/?page=2&page_size=20
    """

    page_size = 20

    page_size_query_param = "page_size"

    max_page_size = 100