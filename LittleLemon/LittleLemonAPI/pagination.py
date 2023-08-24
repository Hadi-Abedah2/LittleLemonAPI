from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10  # default page size
    page_size_query_param = 'perpage'  # allow ?page_size=2, for example
    max_page_size = 100