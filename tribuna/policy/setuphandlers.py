#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plone import api

def runCustomCode(site):
    """ Run custom add-on product installation code to modify Plone site object and others

    @param site: Plone site
    """

    api.user.create(username="tags_user", roles=("Member", ), email="tags_user2@tags.com")
    api.user.grant_roles(username="tags_user", roles=["Site Administrator", "Member", "Manager", "Editor", "Reader", "Contributor", "Reviewer"])



def setupVarious(context):
    """
    @param context: Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('your.package.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    runCustomCode(portal)
