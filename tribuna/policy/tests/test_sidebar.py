#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sidebar tests for this package."""

from tribuna.policy.testing import IntegrationTestCase
from tribuna.policy.testing import Session
from plone import api


class TestSidebar(IntegrationTestCase):
    """Test the sidebar functionality."""

    """
        Workflows don't work in tests! Need to publish everything on create
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.session = self.portal.session_data_manager = Session()

        # Create some tags and articles
        self.tags_folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="Tags",
        )
        for i in range(10):
            api.content.create(
                container=self.tags_folder,
                type="tribuna.content.tag",
                title="Tag {0}".format(i+1),
            )

        self.articles_folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="Articles",
        )
        # Articles with one tag
        for i in range(5):
            api.content.create(
                container=self.articles_folder,
                type="tribuna.content.article",
                title="Article {0}".format(i+1),
                subject=["Tag {0}".format(i+1)],
            )
        # Articles with two tags
        for i in range(5):
            api.content.create(
                container=self.articles_folder,
                type="tribuna.content.article",
                title="Article {0} {1}".format(i+1, i+2),
                subject=["Tag {0}".format(i+1), "Tag {0}".format(i+2)],
            )
        # Articles with three tags
        for i in range(5):
            api.content.create(
                container=self.articles_folder,
                type="tribuna.content.article",
                title="Article {0} {1} {2}".format(i+1, i+2, i+3),
                subject=[
                    "Tag {0}".format(i+1),
                    "Tag {0}".format(i+2),
                    "Tag {0}".format(i+3)
                ],
            )
        # Articles with four tags
        for i in range(5):
            api.content.create(
                container=self.articles_folder,
                type="tribuna.content.article",
                title="Article {0} {1} {2} {3}".format(i+1, i+2, i+3, i+4),
                subject=[
                    "Tag {0}".format(i+1),
                    "Tag {0}".format(i+2),
                    "Tag {0}".format(i+3),
                    "Tag {0}".format(i+4)
                ],
            )

    def test_no_session(self):
        import pdb; pdb.set_trace()
        pass


        # api.content.create(
        #     container=self.portal,
        #     type='tribuna.content.tag',
        #     title="Tag 1")
