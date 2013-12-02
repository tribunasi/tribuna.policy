# -*- coding: utf-8 -*-

from plone import api
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from Products.ResourceRegistries.exportimport.resourceregistry import \
    importResRegistry
from tribuna.content.portlets.sidebar import Assignment
from tribuna.policy.config import INITIAL_STRUCTURE
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.container.interfaces import INameChooser


def create_tags_user(portal):
    """Create tags user, which is needed for working with tags.

    XXX: Make it work without this!

    :param site: Plone site
    """

    api.user.create(
        username="tags_user", roles=("Member", ), email="info@termitnjak.si")
    api.user.grant_roles(
        username="tags_user",
        roles=[
            "Site Administrator",
            "Member",
            "Manager",
            "Editor",
            "Reader",
            "Contributor",
            "Reviewer",
        ]
    )


def create_structure(portal):
    """Create folder structure."""

    # delete default Plone content
    for item_id in ('Members', 'news', 'events', 'front-page'):
        try:
            api.content.delete(portal[item_id])
        except KeyError:
            pass

    # create root folders
    for item in INITIAL_STRUCTURE:
        obj = api.content.create(
            container=portal,
            type=item['type'],
            title=item['title'],
        )
        # XXX: This is probably a bug in plone.api, the title is not set
        # correctly, we need to set it again (id is created correctly tho)
        obj.title = item['title']
        api.content.transition(obj, transition='publish')

    # create an entry page and set it as default view
    entry_page = api.content.create(
        container=portal['entry-pages'],
        type='tribuna.content.entrypage',
        title='Hello',
        text=u'Hello'
    )
    api.content.transition(entry_page, transition='publish')
    portal['entry-pages'].setDefaultPage(entry_page.id)

    # set default view also on root
    portal.default_page = 'entry-pages'


def add_sidebar_portlet(portal):
    """Add sidebar portlet (with tags, filters etc.) and block all other
    portlets.
    """
    # Block parent portlets
    for col in (u'plone.rightcolumn', u'plone.leftcolumn', ):
        portlet_manager = getUtility(
            IPortletManager, name=col, context=portal)
        assignable = getMultiAdapter(
            (portal, portlet_manager,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # Create a sidebar portlet assignment
    mapping = getMultiAdapter(
        (portal, portlet_manager,),
        IPortletAssignmentMapping,
        context=portal
    )
    assignment = Assignment()
    chooser = INameChooser(mapping)
    mapping[chooser.chooseName(None, assignment)] = assignment


def setup_various(context):
    if context.readDataFile('tribuna.policy.setup_various.txt') is None:
    # Not our add-on
        return
    portal = api.portal.get()
    create_tags_user(portal)
    create_structure(portal)
    add_sidebar_portlet(portal)


def reset_css_registry(context):
    """Remove all resources from the CSS registry and add them from
    cssregistry.xml.
    """
    if context.readDataFile('tribuna.policy.setup_various.txt') is None:
    # Not our add-on
        return
    portal_css = api.portal.get_tool('portal_css')
    portal_css.clearResources()

    return importResRegistry(
        context,
        'portal_css',
        'Tribuna CSS registry',
        'cssregistry.xml'
    )


def reset_js_registry(context):
    """Remove all resources from the JavaScript registry and add them
    from jsregistry.xml.
    """
    if context.readDataFile('tribuna.policy.setup_various.txt') is None:
    # Not our add-on
        return
    portal_js = api.portal.get_tool('portal_javascripts')
    portal_js.clearResources()
    return importResRegistry(
        context,
        'portal_javascripts',
        'Tribuna Javascript registry',
        'jsregistry.xml'
    )
