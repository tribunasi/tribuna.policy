# -*- coding: utf-8 -*-
"""View tests."""

from plone import api

from tribuna.policy.testing import IntegrationTestCase
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

    # XXX: indexes don't work in tests, couldn't fix em (adding to catalog.xml
    # etc. didn't help). Can enable them when we get the
    # .highlight_in_navigation index working ...
    #
    # def test_home_view_without_get(self):
    #     """Test view wihout GET parameters, should get articles with
    #     highlighted tags."""

    #     self.assertEqual(self.view.is_text_view(), False)

    #     articles = self.view._get_articles()
    #     self.assertEqual(articles['all'], [])
    #     self.assertEqual(articles['intersection'], [])
    #     self.assertEqual(articles['union'], [])

    # def test_homepage_view_populated_session(self):
    #     """Test view with populated session."""
    #     # Testing the is_text_view function
    #     self.session.set('view_type', 'drag')
    #     self.assertEqual(self.view.is_text_view(), False)
    #     self.session.set('view_type', 'text')
    #     self.assertEqual(self.view.is_text_view(), True)
    #     self.session.set('view_type', 'justsomethingbla14')
    #     self.assertEqual(self.view.is_text_view(), True)


class TestTagsViewEmpty(IntegrationTestCase):
    """Test empty tags view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = api.content.get_view(
            name="tags",
            context=self.portal,
            request=self.layer['request']
        )

    def test_tags_view_without_get(self):
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

    def test_tags_view_with_get(self):
        # set GET parameter to text view

        self.view.request.form['view_type'] = 'text'
        self.assertEqual(self.view.is_text_view(), True)


class TestTagsViewPopulated(IntegrationTestCase):
    """Test the populated tags view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        populate_dummy(self.portal)
        self.view = api.content.get_view(
            name="tags",
            context=self.portal,
            request=self.layer['request']
        )

    def test_tags_view_without_get(self):
        """Test view wihtout GET parameters"""
        # XXX: remove this when we get the .highlight_in_navigation index to
        # work
        self.view.request.form['tags'] = 'htag'

        articles = self.view._get_articles()
        articles_all = articles_intersection = [
            self.portal['articles-folder']['article-h'],
            self.portal['articles-folder']['article-h2a'],
        ]
        articles_union = []

        self.assertEqual(
            sorted(articles['all'], key=lambda x: x.title),
            sorted(articles_all, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['intersection'], key=lambda x: x.title),
            sorted(articles_intersection, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['union'], key=lambda x: x.title),
            sorted(articles_union, key=lambda x: x.title)
        )

    def test_tags_view_selected_tags(self):
        """Test tags view with some selected tags"""

        # One tag selected
        self.view.request.form['tags'] = 'tag1'
        articles = self.view._get_articles()
        articles_all = articles_intersection = [
            self.portal['articles-folder']['article-1a'],
            self.portal['articles-folder']['article-1b'],
            self.portal['articles-folder']['article-12a'],
            self.portal['articles-folder']['article-123a'],
        ]
        articles_union = []

        self.assertEqual(
            sorted(articles['all'], key=lambda x: x.title),
            sorted(articles_all, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['intersection'], key=lambda x: x.title),
            sorted(articles_intersection, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['union'], key=lambda x: x.title),
            sorted(articles_union, key=lambda x: x.title)
        )

        # Two tags selected - test union and intersection
        self.view.request.form['tags'] = 'tag2,tag3'
        articles = self.view._get_articles()
        articles_union = [
            self.portal['articles-folder']['article-2a'],
            self.portal['articles-folder']['article-3a'],
            self.portal['articles-folder']['article-12a'],
            self.portal['articles-folder']['article-h2a'],
        ]
        articles_intersection = [
            self.portal['articles-folder']['article-123a'],
        ]
        articles_all = articles_union + articles_intersection

        self.assertEqual(
            sorted(articles['all'], key=lambda x: x.title),
            sorted(articles_all, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['intersection'], key=lambda x: x.title),
            sorted(articles_intersection, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['union'], key=lambda x: x.title),
            sorted(articles_union, key=lambda x: x.title)
        )

        # All tags selected, plus a nonexistent one (which is ignored)
        self.view.request.form['tags'] = 'tag1,tag2,tag3,htag,nonexistent-tag'
        articles = self.view._get_articles()
        articles_all = articles_union = self.portal['articles-folder'].values()
        articles_intersection = []

        self.assertEqual(
            sorted(articles['all'], key=lambda x: x.title),
            sorted(articles_all, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['intersection'], key=lambda x: x.title),
            sorted(articles_intersection, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['union'], key=lambda x: x.title),
            sorted(articles_union, key=lambda x: x.title)
        )

    def test_tags_view_filters(self):
        """Test tags view with some selected filters"""

        # We have no comments, images or annotations
        self.view.request.form['filters'] = 'comment,image,annotation'
        articles = self.view._get_articles()
        self.assertEqual(articles['union'], [])
        self.assertEqual(articles['intersection'], [])
        self.assertEqual(articles['all'], [])

        # But we do have articles
        self.view.request.form['filters'] = 'image,article'
        self.view.request.form['tags'] = 'htag'
        articles = self.view._get_articles()
        articles_intersection = [
            self.portal['articles-folder']['article-h'],
            self.portal['articles-folder']['article-h2a'],
        ]
        articles_union = []
        articles_all = articles_union + articles_intersection

        self.assertEqual(
            sorted(articles['all'], key=lambda x: x.title),
            sorted(articles_all, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['intersection'], key=lambda x: x.title),
            sorted(articles_intersection, key=lambda x: x.title)
        )
        self.assertEqual(
            sorted(articles['union'], key=lambda x: x.title),
            sorted(articles_union, key=lambda x: x.title)
        )


class TestMainPageViewEmpty(IntegrationTestCase):
    """Test empty main view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = api.content.get_view(
            name="articles",
            context=self.portal,
            request=self.layer['request']
        )

    def test_main_view_without_get(self):
        """Test view without GET parameters."""

        articles_all = self.view.articles_all()
        self.assertEqual(articles_all, [])

    def test_main_view_close_button_URL_from_home(self):
        """Test the close button URL when coming from home view"""
        prefix = "http://nohost/plone/"

        # We came from home
        self.view.request.form['came_from'] = 'home'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'home')
        self.view.request.form['view_type'] = 'text'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'home?view_type=text')
        self.view.request.form['view_type'] = 'drag'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'home?view_type=drag')

        # We ignore everything but 'view_type' if we came from home
        self.view.request.form['filters'] = 'comment'
        self.view.request.form['tags'] = 'tag1,tag2'
        self.view.request.form['sth'] = 'sthelse'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'home?view_type=drag')

    def test_main_view_close_button_URL_from_search(self):
        """Test the close button URL when coming from search view"""
        prefix = "http://nohost/plone/"

        # We came from search
        self.view.request.form['came_from'] = 'search'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'search')
        self.view.request.form['view_type'] = 'text'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'search?view_type=text')
        self.view.request.form['view_type'] = 'drag'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'search?view_type=drag')

        # We take other options into account too (even )
        self.view.request.form['filters'] = 'comment'
        self.view.request.form['tags'] = 'tag1,tag2'
        self.view.request.form['sth'] = 'sthelse'
        url = self.view.get_close_url()
        self.assertEqual(
            url,
            (prefix + 'search?sth=sthelse&filters=comment&view_type=drag' +
             '&tags=tag1,tag2')
        )

    def test_main_view_close_button_URL_from_tags(self):
        """Test the close button URL when coming from tags view"""
        prefix = "http://nohost/plone/"

        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'tags/')

        # Tags are a bit special
        self.view.request.form['tags'] = 'tag1,tag2'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'tags/tag1,tag2')

        self.view.request.form['view_type'] = 'text'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'tags/tag1,tag2?view_type=text')
        self.view.request.form['view_type'] = 'drag'
        url = self.view.get_close_url()
        self.assertEqual(url, prefix + 'tags/tag1,tag2?view_type=drag')

        self.view.request.form['filters'] = 'comment'
        self.view.request.form['sth'] = 'sthelse'
        url = self.view.get_close_url()
        self.assertEqual(
            url,
            (prefix + 'tags/tag1,tag2?view_type=drag&sth=sthelse' +
             '&filters=comment')
        )

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


class TestMainPageViewPopulated(IntegrationTestCase):
    """Test the populated home view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        populate_dummy(self.portal)
        self.view = api.content.get_view(
            name="articles",
            context=self.portal,
            request=self.layer['request']
        )

    def test_main_view_without_get(self):
        """Test view without GET parameters"""

        # XXX: remove this when we get the .highlight_in_navigation index to
        # work
        self.view.request.form['tags'] = 'htag'

        # If we viewed an article that doesn't exist
        self.view.article_id = 'nonexistent-article'
        articles_all = self.view.articles_all()
        self.assertEqual(articles_all, [])

        # If we viewed an article that is not in the filters (highlighted),
        # show only the one
        self.view.article_id = 'article-1a'
        articles_all = self.view.articles_all()
        self.assertEqual(
            articles_all,
            [self.portal['articles-folder']['article-1a']]
        )

        # If we viewed an article that is inside the filters (highlighted),
        # show all articles that are in filters
        self.view.article_id = 'article-h'
        articles_all = self.view.articles_all()
        articles = [
            self.portal['articles-folder']['article-h'],
            self.portal['articles-folder']['article-h2a'],
        ]

        self.assertEqual(
            sorted(articles_all, key=lambda x: x.title),
            sorted(articles, key=lambda x: x.title)
        )
