from typing import Iterable, Tuple

from wagtail import VERSION

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Page
else:
    from wagtail.core.models import Page


def build_page_tree(
    # Would that mypy supported recursive types
    tree=Iterable[Tuple[Page, Iterable]],
    root=None
):
    """
    Construct a page tree in the database. Accepts a tree in the form:

        [
            (Page, [
                (Page, [...]),
                (Page, [...]),
                Page,
            ]),
        ]

    where ``[...]`` is a nested iterable of (Page, children) tuples or bare
    page instances.
    """

    created = []

    for node in tree:
        if isinstance(node, Page):
            # If `node` is a bare page, it has no children
            page = node
            children = []
        else:
            # Otherwise assume it is a (Page, children) tuple
            page, children = node

        if root:
            root.add_child(instance=page)
        else:
            type(page).add_root(instance=page)

        created += [page]
        created += build_page_tree(children, root=page)

    return created
