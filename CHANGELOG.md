v1.1.3

* Fix: inverse sorting in QuerySetGallery

v1.1.2

* Fix: drop queryset order_by lookups if there aren't params for lookup

v1.1.1

* #8 Get queryset with additional params

v1.1.0

* #7 Add simple search
* Fix: division by zero error if there are emplty objects and per_page is -1

v1.0.3

* Fix: wrong error handling for queryset ordering

v1.0.2

* Refactoring: rename QuerySetGallery 'get_page' param  from 'sort_params' to 'order_by_lookups'

v1.0.1

* #6 Implement ordering for queryset gallery

v1.0.0

* #5 Implement a possibility to raise not found error 
* Add tests

v0.1.1

* #4 Implement working with models

v0.1.0

* #3 Implement a gallery functionality
* #2 Implement a queryset filtering
* #1 Implement a pagination for queryset
