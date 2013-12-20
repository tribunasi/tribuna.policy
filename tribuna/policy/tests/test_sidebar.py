#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sidebar tests for this package."""
from datetime import datetime
from plone import api

from tribuna.policy.testing import IntegrationTestCase


class TestSidebar(IntegrationTestCase):
    """Test the sidebar functionality."""

    """
        Not tested yet:
        content_filters
        sort_on (as we'll probably remove alphabetical and sorting on comments
            doesn't work yet)
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        custom_minute = 0
        self.portal = self.layer['portal']
        self.session = self.portal.session_data_manager = Session()
        self.workflow = api.portal.get_tool('portal_workflow')
        self.workflow.setDefaultChain('simple_publication_workflow')

        # Create some tags
        self.tags_folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="Tags",
        )
        api.content.transition(obj=self.tags_folder, transition="publish")

        for i in range(10):
            api.content.transition(
                obj=api.content.create(
                    container=self.tags_folder,
                    type="tribuna.content.tag",
                    title="Tag {0}".format(i+1),
                ),
                transition="publish"
            )

        # Create some articles, spoof creation date
        self.articles_folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="Articles",
        )
        api.content.transition(obj=self.articles_folder, transition="publish")
        # Articles with one tag
        for i in range(5):
            api.content.transition(
                obj=api.content.create(
                    container=self.articles_folder,
                    type="tribuna.content.article",
                    title="Article {0}".format(i+1),
                    subject=["Tag {0}".format(i+1)],
                    locked_on_home=False,
                    effective_date=datetime(2013, 11, 7, 12, custom_minute, 0)
                ),
                transition="publish"
            )
            custom_minute += 1
        # Articles with two tags
        for i in range(5):
            api.content.transition(
                obj=api.content.create(
                    container=self.articles_folder,
                    type="tribuna.content.article",
                    title="Article {0} {1}".format(i+1, i+2),
                    subject=["Tag {0}".format(i+1), "Tag {0}".format(i+2)],
                    locked_on_home=False,
                    effective_date=datetime(2013, 11, 7, 12, custom_minute, 0)
                ),
                transition="publish"
            )
            custom_minute += 1
        # Articles with three tags
        for i in range(5):
            api.content.transition(
                obj=api.content.create(
                    container=self.articles_folder,
                    type="tribuna.content.article",
                    title="Article {0} {1} {2}".format(i+1, i+2, i+3),
                    subject=[
                        "Tag {0}".format(i+1),
                        "Tag {0}".format(i+2),
                        "Tag {0}".format(i+3)
                    ],
                    locked_on_home=False,
                    effective_date=datetime(2013, 11, 7, 12, custom_minute, 0)
                ),
                transition="publish"
            )
            custom_minute += 1
        # Articles with four tags
        for i in range(5):
            api.content.transition(
                obj=api.content.create(
                    container=self.articles_folder,
                    type="tribuna.content.article",
                    title="Article {0} {1} {2} {3}".format(i+1, i+2, i+3, i+4),
                    subject=[
                        "Tag {0}".format(i+1),
                        "Tag {0}".format(i+2),
                        "Tag {0}".format(i+3),
                        "Tag {0}".format(i+4)
                    ],
                    locked_on_home=False,
                    effective_date=datetime(2013, 11, 7, 12, custom_minute, 0)
                ),
                transition="publish"
            )
            custom_minute += 1

    def test_no_session(self):
        """Test defaults without a session."""
        from tribuna.content.portlets.sidebar import articles

        # Since no tags are highlighted, it should return an empty list
        article_titles = []
        articles(self.session)
        self.assertEquals(
            [i.title for i in self.session['content_list']['intersection']],
            article_titles
        )

        # Add some highlighted tags and test again

        # for i in range(4, -1, -1):
        #     article_titles.append(
        #         u"Article {0} {1} {2} {3}".format(i+1, i+2, i+3, i+4)
        #     )
        # for i in range(4, -1, -1):
        #     article_titles.append(
        #         u"Article {0} {1} {2}".format(i+1, i+2, i+3)
        #     )
        # for i in range(4, -1, -1):
        #     article_titles.append(
        #         u"Article {0} {1}".format(i+1, i+2)
        #     )

    def test_one_tag(self):
        """Test with one tag selected."""
        from tribuna.content.portlets.sidebar import articles
        from tribuna.policy.testing import session_populate_portlet_data

        session_populate_portlet_data(self.session)
        self.session['portlet_data']['tags'] = [u"Tag 1"]
        # Should return all articles that have the tag "Tag 1", sorted
        # descending on Date
        article_titles = [
            u"Article 1 2 3 4",
            u"Article 1 2 3",
            u"Article 1 2",
            u"Article 1",
        ]

        articles(self.session)
        self.assertEquals(
            [i.title for i in self.session['content_list']['intersection']],
            article_titles
        )

    def test_ascending_descending(self):
        """Test ascending and descending sort."""
        from tribuna.content.portlets.sidebar import articles
        from tribuna.policy.testing import session_populate_portlet_data

        session_populate_portlet_data(self.session)

        # Descending is already tested in previous test, so we only test
        # ascending
        self.session['portlet_data']['sort_order'] = "ascending"
        self.session['portlet_data']['tags'] = [u"Tag 1"]
        # Should return all articles that have the tag "Tag 1", sorted
        # ascending on Date
        article_titles = [
            u"Article 1",
            u"Article 1 2",
            u"Article 1 2 3",
            u"Article 1 2 3 4",
        ]

        articles(self.session)
        self.assertEquals(
            [i.title for i in self.session['content_list']['intersection']],
            article_titles
        )

    def test_intersection_union(self):
        """Test intersection and union."""
        from tribuna.content.portlets.sidebar import articles
        from tribuna.policy.testing import session_populate_portlet_data

        session_populate_portlet_data(self.session)

        # Testing if intersection and union works as expected
        self.session['portlet_data']['tags'] = [u"Tag 1", u"Tag 2", u"Tag 3"]

        article_titles_intersection = [
            u"Article 1 2 3 4",
            u"Article 1 2 3",
        ]
        article_titles_union = [
            u'Article 2 3 4 5',
            u'Article 2 3 4',
            u'Article 2 3',
            u'Article 1 2',
            u'Article 3 4 5 6',
            u'Article 3 4 5',
            u'Article 3 4',
            u'Article 3',
            u'Article 2',
            u'Article 1'
        ]

        articles(self.session)
        self.assertEquals(
            [i.title for i in self.session['content_list']['intersection']],
            article_titles_intersection
        )

        self.assertEquals(
            [i.title for i in self.session['content_list']['union']],
            article_titles_union
        )
