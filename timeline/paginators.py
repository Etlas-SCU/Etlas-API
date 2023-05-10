from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """custom pagination class to limit the number of results returned by the API
    how to use in url:
    add ?limit=5&offset=10 to the end of the url (5 results starting from the 10th result)
    change the values to whatever you want"""
    default_limit = 5
    max_limit = 10

    def get_limit(self, request):
        limit = super().get_limit(request)
        if limit is None or limit > self.max_limit:
            return self.max_limit
        return limit
