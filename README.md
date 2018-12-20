# Wagtail Foliage

[![CircleCI](https://circleci.com/gh/harrislapiroff/wagtail-foliage.svg?style=svg)](https://circleci.com/gh/harrislapiroff/wagtail-foliage)

Utilities for programmatically building page trees in Wagtail for automated
tests, default site structures, and more.

## Requirements

Wagtail Foliage supports:

* Python 3.4, 3.5, 3.6, and 3.7
* Django 1.11, 2.0, and 2.1
* Wagtail 1.13, 2.3, and 2.4

These are the currently supported versions for each project as of December
2018, excepting the exclusion of Python 2.7 from this list.

## Installation

```shell
pip install wagtail-foliage
```

## Usage

### Use as a context manager

```python
from django.db import TestCase
from foliage.contextmanagers import page_tree

from myapp.models import HomePage, InsidePage


class MyAppTestCase(TestCase):
    def test_with_pages(self):
        PAGES = [
            (HomePage(title='Home Page'), [
                InsidePage(title='Inside Page'),
                (InsidePage(title='Inside Page With Children'), [
                    InsidePage(title='Third Level Page'),
                    InsidePage(title='Another Third Level Page')
                ])
            ])
        ]
        with page_tree(PAGES):
            # Tests that rely on that page tree go here. The context manager
            # will automatically set the top level page as the Wagtail site's
            # root page
```

### Use as a decorator

```python
from django.db import TestCase
from foliage.contextmanagers import page_tree

from myapp.models import HomePage, InsidePage


PAGES = [
    (HomePage(title='Home Page'), [
        InsidePage(title='Inside Page'),
        (InsidePage(title='Inside Page With Children'), [
            InsidePage(title='Third Level Page'),
            InsidePage(title='Another Third Level Page')
        ])
    ])
]


class MyAppTestCase(TestCase):
    @page_tree(PAGES)
    def test_with_pages(self):
        # Tests that rely on that page tree go here. The context manager
        # will automatically set the top level page as the Wagtail site's
        # root page
```

### Use the low-level API

```python
from foliage.utils import build_page_tree

from myapp.models import HomePage, InsidePage

new_pages = build_page_tree([
    (HomePage(title='Home Page'), [
        InsidePage(title='Inside Page'),
        (InsidePage(title='Inside Page With Children'), [
            InsidePage(title='Third Level Page'),
            InsidePage(title='Another Third Level Page')
        ])
    ])
])
```
