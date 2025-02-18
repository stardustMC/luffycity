from rest_framework.pagination import PageNumberPagination


class CoursePageNumberPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'size'

