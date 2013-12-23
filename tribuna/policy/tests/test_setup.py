# -*- coding: utf-8 -*-
"""Setup/installation tests."""

from tribuna.policy.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of tribuna.policy into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tribuna.policy is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('tribuna.policy'))

    def test_uninstall(self):
        """Test if tribuna.policy is cleanly uninstalled."""
        self.installer.uninstallProducts(['tribuna.policy'])
        self.assertFalse(self.installer.isProductInstalled('tribuna.policy'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ITribunaPolicyLayer is registered."""
        from tribuna.policy.interfaces import ITribunaPolicyLayer
        from plone.browserlayer import utils
        self.failUnless(ITribunaPolicyLayer in utils.registered_layers())

    def test_initial_content(self):
        """Test if the initial content hierachy was installed properly"""
        assert 'tags-folder' in self.portal.keys()
        assert 'articles-folder' in self.portal.keys()
        assert 'images-folder' in self.portal.keys()
        assert 'entry-pages' in self.portal.keys()
        assert 'files-folder' in self.portal.keys()
