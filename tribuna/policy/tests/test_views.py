# -*- coding: utf-8 -*-
"""View tests."""

from plone import api
from tribuna.policy.testing import IntegrationTestCase
from tribuna.policy.testing import create_article
from tribuna.policy.testing import populate_dummy


class TestHomePageViewEmpty(IntegrationTestCase):
    """Test empty home view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = api.content.get_view(
            name="home",
            context=self.portal,
            request=self.layer['request']
        )

    def test_home_view_without_get(self):
        """Test view without GET parameters."""
        # defaults to drag view
        self.assertEqual(self.view.is_text_view(), False)

        # check for empty articles
        articles = self.view._get_articles()
        self.assertEqual(articles['union'], [])
        self.assertEqual(articles['intersection'], [])
        self.assertEqual(articles['all'], [])

        self.assertEqual(self.view.show_intersection(), False)
        self.assertEqual(self.view.show_union(), False)

    def test_home_view_with_get(self):
        # set GET parameter to text view

        self.view.request.form['view_type'] = 'text'
        self.assertEqual(self.view.is_text_view(), True)


class TestHomePageViewPopulated(IntegrationTestCase):
    """Test the populated home view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        populate_dummy(self.portal)
        self.view = api.content.get_view(
            name="home",
            context=self.portal,
            request=self.layer['request']
        )

    def test_home_view_without_get(self):
        """Test view wihout GET parameters, should get articles with
        highlighted tags."""

        self.assertEqual(self.view.is_text_view(), False)

        articles = self.view._get_articles()
        self.assertEqual(articles['all'], [])
        self.assertEqual(articles['intersection'], [])
        self.assertEqual(articles['union'], [])

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
        #
        #
        #
        #
        # Need to rewrite this, the way we get the content has changed
        # (no more content_list in session etc.)
        #
        #
        #
        articles_union = ["Article 1", "Article 2", "Article 3"]
        articles_intersection = ["Article 1i", "Article 2i", "Article 3i"]
        self.session.set('content_list', {'union': [], 'intersection': []})
        self.session['content_list']['union'] = articles_union
        self.session['content_list']['intersection'] = articles_intersection

        articles = self.view._get_articles()
        self.assertEqual(articles['union'], articles_union)
        self.assertEqual(articles['intersection'],
                         articles_intersection)
        self.assertEqual(articles['all'],
                         articles_intersection + articles_union)

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
            name="articles",
            context=self.portal,
            request=self.layer['request']
        )

    def test_mainpage_view_empty_session(self):
        """Test view with empty session."""
        self.assertEqual(self.view.articles_all(), [])

    def test_mainpage_view_populated_session(self):
        """Test view with populated session."""
        articles = ["Article 1", "Article 2", "Article 3"]
        self.session.set('content_list', {'union': [], 'intersection': []})
        self.session['content_list']['intersection'] = articles[:2]
        self.session['content_list']['union'] = articles[2:]
        self.assertEqual(self.view.articles_all(), articles)

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
