# Django-queryset-gallery

Queryset gallery is an interface for creating a gallery that provides pagination and filtering via lookups. It can be useful for getting objects via API.

## Table of contents

* [How to create filters](#how-to-create-filters)
* [How to create a gallery](#how-to-create-a-gallery)
* [How to use simple search](#how-to-use-simple-search)
* [How to work with pagination](#how-to-work-with-pagination)

### How to create filters

Every filter inherits from base class `QuerySetFilter` and include two args: `key` and `lookup`. Filters apply via standard method queryset method `filter`. So, `lookup` will be used for filtering. `key` is an id of a filter and it is used when you provide to gallery engine dict with params for filtering. A filter gets param from dict via `key`.

```
from queryset_gallery.filters import QuerySetFilter

UserEmail = QuerySetFilter(
    key='email',
    lookup='email__icontains'
)
UserIsStaff = QuerySetFilter(
    key='is_staff',
    lookup='is_staff'
)
```

### How to create a gallery

A base class for a gallery in `QuerySetGallery`. When you need to create a gallery you provide django `model` and set `QuerySetFilter` objects in `filters` conts:

```
from django.contrib.auth.models import User
from queryset_gallery.gallery import QuerySetGallery

class UserGallery(QuerySetGallery):
    model = User
    filters = [UserEmail, UserIsStaff]
```

The gallery has a method `get_page`. It gets several params like:

```
def get_page(self, page_number, per_page, filter_params: dict = None, order_by_lookups: list = None, queryset_params=None, queryset=None):
```

The first and second args are params for paginator. The third arg `filter_params` is a dict with params for filters. It includes filter keys and params. Also, you can provide source `queryset` or override method `get_queryset`, by default all model objects will be used as a source. Also, if there additional params for getting queryset you can provide it via `queryset_params`. The last arg `order_by_lookups` is a list of lookups for queryset method `order_by()`. All lookups from a list will be applied to queryset. Finally the gallery return queryset and dict of pagination data.

```
gallery = UserGallery()
filter_params = {
    'email': 'admin',
    'is_staff': True,
}

gallery.get_page(per_page=10, page_number=1, filter_params=params, order_by_lookups=['email'])
```

### How to use simple search

The simple search is a situation then there a list of params list `['Alex', 'Ambassador']` and several fields for filtering, for example, `first_name`, `last_name` and `nickname`. `QuerySetGallery` supports a simple search via `QuerySetSimpleSearch`. It's just a filter that can be added to const `filters`. For the example above `QuerySetSimpleSearch` create several Django Q objects with a condition OR and execute them. `QuerySetSimpleSearch` is created in the same way as `QuerySetFilter` but get a list of lookups instead of one lookup:

```
from django.contrib.auth.models import User

users = User.objects.all()

UserSimpleSearch = QuerySetSimpleSearch(
    key='query',
    lookups=[
        'first_name__icontains',
        'last_name__icontains',
        'nickname__icontains'
    ]
)
UserSimpleSearch.apply(users, ['Alex', 'Ambassador'])
```

### How to work with pagination

You don't need to work with `Paginator`, because the `QuerySetGallery` class works with it. The `QuerySetGallery` has two nuances. If you want to get all objects you can set `per_page` as -1. This way pagination returns all objects. If `per_page` and `necessary_page` are invalid it raises error 404.

Example of the pagination data:

```
data =  {
    'objects_count': 20,
    'page_number': 2,
    'page_count': 1,
    'per_page': 100,
}
```
