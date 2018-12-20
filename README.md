# Wagtail Foliage

Utilities for programmatically building page trees in Wagtail.

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
