# Wagtail Foliage

Utilities for programmatically building page trees in Wagtail.

## Usage

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
