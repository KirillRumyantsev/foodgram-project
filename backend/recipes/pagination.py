from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Кастомный паджинатор.
    """

    page_size_query_param = 'limit'
