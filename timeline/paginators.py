from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10

    def get_limit(self, request):
        limit = super().get_limit(request)
        if limit is None or limit > self.max_limit:
            return self.max_limit
        return limit
