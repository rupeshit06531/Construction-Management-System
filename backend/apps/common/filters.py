from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """
    Supports comma separated IDs.

    Example:
    ?id__in=1,2,3
    """
    pass


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    """
    Supports comma separated text values.

    Example:
    ?status__in=ACTIVE,PENDING
    """
    pass