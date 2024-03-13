from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rest_framework.request import Request

from rest_framework import pagination
from rest_framework.response import Response


class StandardResultSetPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    page_query_param = "page"
    page_size = 50
    max_page_size = 5000

    def set_page_size(self, request: "Request"):
        page_size = request.query_params.get(self.page_size_query_param, self.page_size)
        self.page_size = int(page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "page_size": self.page_size,
                "total_objects": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
