# -*- coding: utf-8 -*-
"""Tests for behaviors."""

from tribuna.policy.testing import IntegrationTestCase
from tribuna.policy.testing import create_article


class TestBehaviors(IntegrationTestCase):
    """Test the Tag content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_itag_behavior(self):
        """Test ITag behavior (automatic tag generation and "normalisation" of
        tags.
        """

        create_article(
            container=self.portal['articles-folder'],
            title="Article",
            subject=['tag1', 'tag2']
        )

        # Check if the behavior set tags correctly
        self.assertEqual(
            self.portal['articles-folder']['article'].subject,
            ('tag1', 'tag2')
        )

        # Check if the tags were created
        self.assertEqual(
            sorted(self.portal['tags-folder'].keys()),
            ['tag1', 'tag2']
        )

        # Checking if tag normalisation works
        create_article(
            container=self.portal['articles-folder'],
            title="Article",
            subject=['TAG1', 't   a  G2']
        )

        # Tags should be normalised to 'tag1' and 'tag2'
        self.assertEqual(
            self.portal['articles-folder']['article-1'].subject,
            ('tag1', 'tag2')
        )

        # No new tags should be created
        self.assertEqual(
            sorted(self.portal['tags-folder'].keys()),
            ['tag1', 'tag2']
        )

        # Check if a mix of normalised and new tags works
        create_article(
            container=self.portal['articles-folder'],
            title="Article",
            subject=['TAG1', 'tag3', 't   a  G2']
        )
        self.assertEqual(
            self.portal['articles-folder']['article-2'].subject,
            ('tag1', 'tag2', 'tag3')
        )

        # We should have one new tag
        self.assertEqual(
            sorted(self.portal['tags-folder'].keys()),
            ['tag1', 'tag2', 'tag3']
        )
