from wagtail import VERSION

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Page
else:
    from wagtail.core.models import Page


class HomePage(Page):
    pass


class InsidePage(Page):
    pass
