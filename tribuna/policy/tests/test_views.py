#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""View tests for this package."""

from tribuna.policy.testing import IntegrationTestCase
from tribuna.policy.testing import Session
from plone import api


class TestHomePageView(IntegrationTestCase):
    """Test the home-page view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.session = self.portal.session_data_manager = Session()
        self.view = api.content.get_view(
            name="home-page",
            context=self.portal,
            request=self.layer['request']
        )

    def test_homepage_view_empty_session(self):
        """Test view with empty session."""
        self.assertEqual(self.view.is_text_view(), True)
        self.assertEqual(self.view.articles(), [])
        self.assertEqual(self.view.only_one_tag(), False)
        # We do not test tag_description, as it only runs when only_one_tag
        # returns True

    def test_homepage_view_populated_session(self):
        """Test view with populated session."""
        # Testing the is_text_view function
        self.session.set('view_type', 'drag')
        self.assertEqual(self.view.is_text_view(), False)
        self.session.set('view_type', 'text')
        self.assertEqual(self.view.is_text_view(), True)
        self.session.set('view_type', 'justsomethingbla14')
        self.assertEqual(self.view.is_text_view(), True)

        # Testing the articles function
        articles = ["Article 1", "Article 2", "Article 3"]
        self.session.set('content_list', articles)
        self.assertEqual(self.view.articles(), articles)

        # Testing the only_one_tag function
        self.session['portlet_data'] = Session()
        self.session['portlet_data']['tags'] = ["Tag 1", "Tag 2"]
        self.assertEqual(self.view.only_one_tag(), False)
        tag = api.content.create(
            container=self.portal,
            type='tribuna.content.tag',
            title="Tag 1")
        self.session['portlet_data']['tags'] = ["Tag 1"]
        self.assertEqual(self.view.only_one_tag(), True)
        self.assertEqual(self.view.tag_description(),
                         u"Description not added yet!")
        tag.description = u"Test description"
        self.assertEqual(self.view.tag_description(), u"Test description")


class TestMainPageView(IntegrationTestCase):
    """Test the main-page view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.session = self.portal.session_data_manager = Session()
        self.view = api.content.get_view(
            name="main-page",
            context=self.portal,
            request=self.layer['request']
        )

    def test_mainpage_view_empty_session(self):
        """Test view with empty session."""
        self.assertEqual(self.view.articles(), [])

    def test_mainpage_view_populated_session(self):
        """Test view with populated session."""
        articles = ["Article 1", "Article 2", "Article 3"]
        self.session.set('content_list', articles)
        self.assertEqual(self.view.articles(), articles)

    def test_update(self):
        """Test the update function."""
        # First we test that the disables aren't set yet
        self.assertTrue('disable_plone.rightcolumn' not in self.view.request)
        self.assertTrue('disable_plone.leftcolumn' not in self.view.request)
        self.assertTrue('disable_border' not in self.view.request)

        self.view.update()

        #After updating, the requests should be set on 1
        self.assertEquals(self.view.request['disable_plone.rightcolumn'], 1)
        self.assertEquals(self.view.request['disable_plone.leftcolumn'], 1)
        self.assertEquals(self.view.request['disable_border'], 1)
