from django.db import transaction

from foliage.utils import build_page_tree, get_site, get_root_page


class page_tree(transaction.Atomic):
    def __init__(self, tree, site=None, using=None, savepoint=True):
        if len(tree) > 1:
            raise ValueError("page_tree expects a tree with a single "
                             "root page. Found {}".format(len(tree)))

        self.tree = tree
        self.site = site if site is not None else get_site()
        self.root_page = get_root_page()
        super().__init__(using, savepoint)

    def __enter__(self):
        super().__enter__()  # Start the transaction *first*

        # Find the current site root page (n.b., this is distinct from
        # the wagtail instance's root page at self.root_page)
        old_root_page = self.site.root_page

        # Build the specified page tree under the instance root page and
        # attach it to the wagtail site
        created_pages = build_page_tree(self.tree, self.root_page)
        self.site.root_page = created_pages[0]
        self.site.save()

        # Delete the old root page and any of its descendants
        old_root_page.delete()

    def __exit__(self, exc_type, exc_value, traceback):
        # Trigger a transaction rollback to undo all database changes within
        # this context manager
        transaction.set_rollback(True, using=self.using)
        super().__exit__(exc_type, exc_value, traceback)
