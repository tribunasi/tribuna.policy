# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from tribuna.policy.testing import IntegrationTestCase
from plone import api


class TestTag(IntegrationTestCase):
    """Test the Tag content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_create_tag(self):
        """Test if we can create Tag objects without error."""
        api.content.create(
            container=self.portal, type='tribuna.content.tag', title="Tag 1")


class TestEntryPage(IntegrationTestCase):
    """Test the EntryPage content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_old_entry_pages_no_folder(self):
        """Test getting old entry pages if there is no folder for entry
        pages.
        """
        from tribuna.content.entrypage import old_entry_pages

        self.assertEquals(old_entry_pages(), [])

    def test_old_entry_pages(self):
        """Test if we get the old entry pages without the current entry page.
        """
        from tribuna.content.entrypage import old_entry_pages

        # create a folder and a couple of entry pages
        api.content.create(
            container=self.portal,
            type='Folder',
            id='entry-pages'
        )
        folder = self.portal['entry-pages']
        api.content.create(
            container=folder,
            type='tribuna.content.entrypage',
            title='Entry page 1'
        )
        api.content.create(
            container=folder,
            type='tribuna.content.entrypage',
            title='Entry page 2'
        )
        api.content.create(
            container=folder,
            type='tribuna.content.entrypage',
            title='Entry page 3'
        )

        # set entry page as default view for the folder
        folder.setDefaultPage(folder['entry-page-1'].id)

        # we should get all entry pages except the current one
        results = old_entry_pages()
        self.assertEquals(
            sorted(results),
            [('entry-page-2', 'Entry page 2'),
             ('entry-page-3', 'Entry page 3')]
        )

        