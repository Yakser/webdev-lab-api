from rest_framework import pagination


class CommentsPagination(pagination.LimitOffsetPagination):
    """
    Pagination for Comments

    For example:
        /comments/?limit=10&offset=10
        gets the next 10 comments after the first 10 comments.
    """

    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
