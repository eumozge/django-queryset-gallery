from math import ceil


class Paginator(object):
    """Use for creating yours paginator

    Args:
        `objects` (iterator): objects that must be paginated
        `per_page` (int): objects per page. If `per_page` equals -1 it returns all objects

    Methods:
        `get_page`: get objects per necessary page and dict of pagination data

    Usage:
        ```
        >>> from objects.paginator import Paginator
        >>> p = Paginator([i for i in range(1, 6)], 2)
        >>> p.get_page(3)
        ([5], {'objects_count': 5, 'page_number': 3, 'page_count': 3, 'per_page': 2})
        ```

    """
    __slots__ = ('objects', 'objects_count', 'per_page', 'page_count')

    def __init__(self, objects, per_page=100):
        self.objects = objects
        self.objects_count = self._get_objects_length()
        self.per_page = per_page if per_page != -1 else self.objects_count
        self.page_count = ceil(self.objects_count / self.per_page)

    def _get_objects_length(self) -> int:
        """Use for getting page count"""
        return len(self.objects)

    def _slice_objects(self, start, end):
        return self.objects[start: end]

    def _get_empty_page(self):
        """Use for cases then there is invalid input data"""
        return self._slice_objects(0, 0)

    def _get_objects_for_page(self, number):
        """Slice objects with calculated indexes"""
        start, end = self._calculate_index(number, self.per_page)
        return self._slice_objects(start, end)

    def _is_page_valid(self, necessary_page):
        return self.per_page > 1 and 0 < necessary_page <= self.page_count

    @staticmethod
    def _calculate_index(page_number, per_page):
        start = (page_number - 1) * per_page if page_number > 1 else 0
        end = start + per_page
        return start, end

    def get_page(self, number):
        pagination_data = {
            'objects_count': self.objects_count,
            'page_number': number,
            'page_count': self.page_count,
            'per_page': self.per_page,
        }

        if self._is_page_valid(number):
            objects = self._get_objects_for_page(number)
        else:
            objects = self._get_empty_page()
            pagination_data['errors'] = 'Page data is invalid'

        return objects, pagination_data


class QuerySetPaginator(Paginator):
    """Good for queryset pagination because of slicing

    Args:
        `queryset` (queryset): queryset that must be paginated
        `per_page` (int): the same as for Paginator

    Usage:
        ```
        paginator = PaginationQuerySet(queryset, 10)
        queryset, pagination_data = paginator.get_page(2)
        ```
    """
    def __init__(self, queryset, per_page=100):
        super().__init__(queryset.distinct(), per_page)

    def _get_objects_length(self):
        return self.objects.count()
