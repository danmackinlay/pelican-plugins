# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

# From django.core.paginator
from math import ceil


class Paginator(object):
    def __init__(self, object_list, per_page, orphans=0):
        self.object_list = object_list
        self.per_page = per_page
        self.orphans = orphans
        self._num_pages = self._count = None

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
            self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            hits = max(1, self.count - self.orphans)
            self._num_pages = int(ceil(hits / (float(self.per_page) or 1)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return list(range(1, self.num_pages + 1))
    page_range = property(_get_page_range)


class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page