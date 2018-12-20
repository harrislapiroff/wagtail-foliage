from django.test import TestCase

from wagtail import VERSION

from foliage.contextmanagers import page_tree

from .testapp.models import HomePage, InsidePage

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Site
else:
    from wagtail.core.models import Site


class PageTreeTestCase(TestCase):
    def test_page_tree(self):
        site = Site.objects.get()

        home_page = HomePage(title="Home Page")
        inside_page_1 = InsidePage(title="Page 1")
        inside_page_2 = InsidePage(title="Page 2")

        with page_tree([(home_page, [inside_page_1, inside_page_2])]):
            # Assert that the tree got created underneath the site
            # as expected
            site.refresh_from_db()
            self.assertEqual(
                site.root_page.specific,
                home_page,
            )
            self.assertCountEqual(
                site.root_page.get_children().specific(),
                (inside_page_1, inside_page_2)
            )

        site.refresh_from_db()
        # Assert that the tree got rolled back after the context manager exited
        self.assertNotEqual(site.root_page.specific, home_page)

    def test_page_tree__too_many_roots(self):
        home_page_1 = HomePage(title="Home Page 1")
        home_page_2 = HomePage(title="Home Page 2")

        with self.assertRaises(ValueError) as cm:
            with page_tree([home_page_1, home_page_2]):
                pass

        self.assertSequenceEqual(
            cm.exception.args,
            ("page_tree expects a tree with a single root page. Found 2",)
        )
