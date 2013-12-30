# -*- coding: utf-8 -*-
"""Sidebar tests."""

from plone import api

from tribuna.content.config import SEARCHABLE_TYPES
from tribuna.content.utils import tags_published
from tribuna.policy.testing import IntegrationTestCase
from tribuna.policy.testing import populate_dummy


class TestSidebarFormValuesEmpty(IntegrationTestCase):
    """Test values for the form"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = api.content.get_view(
            name="tribuna-sidebar",
            context=self.portal,
            request=self.layer['request']
        )

    def test_sidebar_form(self):
        """Test sidebar form values"""

        # XXX: Add tests for highlighted tags when you fix the index
        self.assertEqual(tags_published(), ())


class TestSidebarFormValuesPopulated(IntegrationTestCase):
    """Test values for the form"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        populate_dummy(self.portal)
        self.view = api.content.get_view(
            name="tribuna-sidebar",
            context=self.portal,
            request=self.layer['request']
        )

    def test_sidebar_form(self):
        """Test sidebar form values"""

        # XXX: Add tests for highlighted tags when you fix the index
        published_tags = ['htag', 'tag1', 'tag2', 'tag3']
        self.assertEqual(
            sorted([i[0] for i in tags_published()]),
            sorted(published_tags)
        )


class TestSidebar(IntegrationTestCase):
    """Test sidebar."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = api.content.get_view(
            name="tribuna-sidebar",
            context=self.portal,
            request=self.layer['request']
        )

    def form_defaults(self):
        """Mock defaults for the form"""
        self.view.request.form = {}
        self.view.request.form['form.widgets.tags'] = []
        # self.view.request.form['form.widgets.all_tags'] = []
        self.view.request.form['form.widgets.sort_on'] = ['latest']
        self.view.request.form['form.widgets.view_type'] = ['drag']
        self.view.request.form['form.widgets.content_filters'] =\
            ['all'] + SEARCHABLE_TYPES.keys()
        self.view.request.form['form.widgets.query'] = ''
        self.view.request.form['form.widgets.clicked_tag'] = False

    def form_defaults_search(self):
        self.form_defaults()
        self.view.request.form['form.widgets.query'] = 'test-query'

    def test_URL_construction_home(self):
        """Test URL construction functions when we are on home view"""

        # Mock home view URL
        self.view.request.URL = self.portal.portal_url() + '/home'

        # Set defaults
        self.form_defaults()

        # If we clicked on text view button
        self.view.request.form['form.widgets.view_type'] = ['text']
        self.view.request.form['form.buttons.text'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            self.portal.portal_url() + '/home?view_type=text'
        )

        self.form_defaults()

        # If we clicked on drag view button
        self.view.request.form['form.widgets.view_type'] = ['drag']
        self.view.request.form['form.buttons.drag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            self.portal.portal_url() + '/home?view_type=drag'
        )

        self.form_defaults()

        # If we changed content filters
        self.view.request.form['form.widgets.content_filters'] = ['comment']
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags?filters=comment' +
             '&sort_on=latest&view_type=drag')
        )

        self.form_defaults()

        # If we clicked on a tag
        self.view.request.form['form.widgets.all_tags'] = ['tag1']
        self.view.request.form['form.widgets.clicked_tag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags/tag1?filters=comment,article,' +
             'image,annotation&sort_on=latest&view_type=drag')
        )

        self.form_defaults()

        # If we searched for something
        self.view.request.form['form.widgets.query'] = 'test-query'
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=drag')
        )

    def test_URL_construction_search(self):
        """Test URL construction functions when we are on search view"""

        # Mock home view URL
        self.view.request.URL = self.portal.portal_url() + '/search'

        self.form_defaults_search()

        # Defaults
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=drag')
        )

        self.form_defaults_search()

        # If we clicked on text view button
        self.view.request.form['form.widgets.view_type'] = ['text']
        self.view.request.form['form.buttons.text'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=text')
        )

        self.form_defaults_search()

        # If we clicked on drag view button
        self.view.request.form['form.widgets.view_type'] = ['drag']
        self.view.request.form['form.buttons.drag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=drag')
        )

        self.form_defaults_search()

        # If we changed content filters
        self.view.request.form['form.widgets.content_filters'] = ['image']
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=image&sort_on=latest&view_type=drag')
        )

        self.form_defaults_search()

        # If we clicked on the use filters button
        self.view.request.form['form.widgets.use_filters'] = ['selected']
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=drag&use_filters=selected')
        )

        self.form_defaults_search()
        self.view.request.form['form.widgets.all_tags'] = ['tag1']

        # If we added/removed a tag (clicked on the + or -)
        self.view.request.form['form.widgets.all_tags'] += ['tag2']
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?tags=tag1,tag2' +
             '&query="test-query"&filters=comment,article,image,annotation' +
             '&sort_on=latest&view_type=drag')
        )

        self.form_defaults_search()
        self.view.request.form['form.widgets.all_tags'] = ['tag1']

        # If clicked on the tag name
        self.view.request.form['form.widgets.all_tags'] = ['tag2']
        self.view.request.form['form.widgets.clicked_tag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags/tag2?filters=comment,article,' +
             'image,annotation&sort_on=latest&view_type=drag')
        )

    def test_URL_construction_tags(self):
        """Test URL construction functions when we are on tags view"""

        # Mock home view URL
        self.view.request.URL = self.portal.portal_url() + '/tags'

        # Set defaults
        self.form_defaults()

        # If we clicked on text view button
        self.view.request.form['form.widgets.view_type'] = ['text']
        self.view.request.form['form.buttons.text'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags?filters=comment,article,' +
             'image,annotation&sort_on=latest&view_type=text')
        )

        self.form_defaults()

        # If we clicked on drag view button
        self.view.request.form['form.widgets.view_type'] = ['drag']
        self.view.request.form['form.buttons.drag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags?filters=comment,article,' +
             'image,annotation&sort_on=latest&view_type=drag')
        )

        self.form_defaults()

        # If we changed content filters
        self.view.request.form['form.widgets.content_filters'] = ['comment']
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags?filters=comment' +
             '&sort_on=latest&view_type=drag')
        )

        self.form_defaults()

        # If we clicked on a tag
        self.view.request.form['form.widgets.all_tags'] = ['tag1']
        self.view.request.form['form.widgets.clicked_tag'] = True
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/tags/tag1?filters=comment,article,' +
             'image,annotation&sort_on=latest&view_type=drag')
        )

        self.form_defaults()

        # If we searched for something
        self.view.request.form['form.widgets.query'] = 'test-query'
        url = self.view.buildURL()
        self.assertEqual(
            url,
            (self.portal.portal_url() + '/search?query="test-query"' +
             '&filters=comment,article,image,annotation&sort_on=latest' +
             '&view_type=drag')
        )
