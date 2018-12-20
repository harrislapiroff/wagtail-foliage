from typing import Iterable, Tuple, List

from wagtail import VERSION

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Page, Site
else:
    from wagtail.core.models import Page, Site


def build_page_tree(
    # Would that mypy supported recursive types
    tree: Iterable[Tuple[Page, Iterable]],
    root: Page = None
) -> List[Page]:
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


def get_site() -> Site:
    try:
        return Site.objects.get()
    except Site.MultipleObjectsReturned:
        # Reraise MultipleObjectsReturned, but with our own message
        raise Site.MultipleObjectsReturned(
            'Foliage can\'t auto-determine the Wagtail Site. '
            'More than one Site exists in the database!'
        )


def get_root_page() -> Page:
    try:
        return Page.objects.get(depth=1)
    except Page.MultipleObjectsReturned:
        # Reraise MultipleObjectsReturned, but with our own message
        raise Site.MultipleObjectsReturned(
            'Foliage can\'t auto-determine the root page. '
            'More than one Page exists with depth 1 in the database!'
        )
