from django.test import TestCase

from wagtail import VERSION

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Page
else:
    from wagtail.core.models import Page

from foliage.utils import build_page_tree

from .testapp.models import HomePage, InsidePage


class BuildPageTreeTestCase(TestCase):
    def test_build_page_tree__return_val(self):
        """
        `build_page_tree` should return a list of all pages created in the
        order that they were created
        """

        page_tree = [
            (HomePage(title="Home Page"), [
                InsidePage(title="Inside Page 1"),
                InsidePage(title="Inside Page 2"),
            ])
        ]
        results = build_page_tree(page_tree)

        # Check the resuls repr against what we expect return results to be
        self.assertEqual(
            '[<HomePage: Home Page>, <InsidePage: Inside Page 1>, '
            '<InsidePage: Inside Page 2>]',
            results.__repr__()
        )

    def test_build_page_tree__database(self):
        """
        `build_page_tree` should save all page nodes to the database
        """

        home_page = HomePage(title="Home Page")
        inside_page_1 = InsidePage(title="Inside Page 1")
        inside_page_2 = InsidePage(title="Inside Page 2")
        inside_page_2_1 = InsidePage(title="Inside Page 2, 1")

        page_tree = [
            (home_page, [
                inside_page_1,
                (inside_page_2, [inside_page_2_1]),
            ])
        ]
        build_page_tree(page_tree)
        data = Page.dump_bulk(HomePage.objects.get())

        self.assertEqual(data[0]['data']['title'], "Home Page")
        # Home page should have exactly two children with the correct titles
        self.assertEqual(len(data[0]['children']), 2)
        self.assertEqual(
            data[0]['children'][0]['data']['title'],
            "Inside Page 1"
        )
        self.assertEqual(
            data[0]['children'][1]['data']['title'],
            "Inside Page 2"
        )
        # Child 1 should have zero children
        self.assertNotIn('children', data[0]['children'][0])
        # Child 2 should have one child with the proper title
        self.assertEqual(len(data[0]['children'][1]['children']), 1)
        self.assertEqual(
            data[0]['children'][1]['children'][0]['data']['title'],
            "Inside Page 2, 1"
        )
