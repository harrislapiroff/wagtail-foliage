from django.test import TestCase

from wagtail import VERSION

from foliage.utils import build_page_tree, get_site, get_root_page

from .testapp.models import HomePage, InsidePage

if VERSION < (2, 0):
    from wagtail.wagtailcore.models import Page, Site
else:
    from wagtail.core.models import Page, Site


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


class GetSiteTestCase(TestCase):
    def test_get_site__success(self):
        "`get_site` should return a Site object under normal circumstances"
        self.assertTrue(isinstance(get_site(), Site))

    def test_get_site__more_than_one(self):
        """
        If there are multiple sites in the database, `get_site` should raise
        a MultipleObjectsReturned exeption
        """
        # Create a second site with a new root page
        root_page = Page.add_root(instance=Page(title="Second Sight"))
        Site.objects.create(
            hostname='secondsight.com',
            port=80,
            root_page=root_page
        )

        with self.assertRaises(Site.MultipleObjectsReturned) as cm:
            get_site()

        self.assertEqual(
            cm.exception.args,
            ("Foliage can't auto-determine the Wagtail Site. "
             "More than one Site exists in the database!",)
        )


class GetRootPageTestCase(TestCase):
    def test_get_root_page__success(self):
        """
        `get_root_page` should return a Page object under normal circumstances
        """
        self.assertTrue(isinstance(get_root_page(), Page))

    def test_get_root_page__more_than_one(self):
        """
        If there are multiple root pages in the database, `get_root_page`
        should raise a MultipleObjectsReturned exception
        """
        # Create a new root page
        Page.add_root(instance=Page(title="Route 2"))

        with self.assertRaises(Site.MultipleObjectsReturned) as cm:
            get_root_page()

        self.assertEqual(
            cm.exception.args,
            ('Foliage can\'t auto-determine the root page. '
             'More than one Page exists with depth 1 in the database!',)
        )
