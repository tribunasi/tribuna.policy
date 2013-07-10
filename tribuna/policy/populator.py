# -*- coding: utf-8 -*-
"""Generate dummy site content. Code taken from http://www.plone-entwicklerhandbuch.de/plone-entwicklerhandbuch/anhang/praxisbeispiele/dummy-inhalte/setup.py/view
"""

from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

import logging
import loremipsum
import os
import random
import urllib2

logger = logging.getLogger('tribuna.policy.populator')


def gen_paragraphs(num=3):
    """Generate random paragraphs."""
    return u'/'.join([p[2] for p in
        loremipsum.Generator().generate_paragraphs(num)])


def gen_sentence():
    """Generate a random sentence."""
    return loremipsum.Generator().generate_sentence()[-1]


def gen_sentences(length=80):
    """Generate random sentences with the specified length."""
    return u'/'.join([s[2] for s in
        loremipsum.Generator().generate_sentences(length)])


def random_image(width, height):
    """Return a random image from lorempixel.com with the specified width
    and height.
    """
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()


def invokeFactory(folder, portal_type, title=None):
    pt = getToolByName(folder, 'plone_utils')
    obj_title = title
    if not obj_title:
        obj_title = gen_sentence()
    obj_id = pt.normalizeString(obj_title)
    if obj_id in folder.objectIds():
        obj_id += str(random.randint(0, 100))
    folder.invokeFactory(portal_type, id=obj_id, title=obj_title)
    folder[obj_id].reindexObject()
    folder[obj_id].setDescription(gen_paragraphs(1))
    return folder[obj_id]


class PopulateView(grok.View):
    """View for creating dummy site hierarchy."""
    grok.context(IPloneSiteRoot)
    grok.require('cmf.ManagePortal')
    grok.name('populate')

    def update(self):
        self.setup_content()
        self.request.response.redirect(self.context.absolute_url())

    def render(self):
        pass

    def setup_content(self):
        logger.info('Setting up dummy site content...')
        self.install_structure()
        logger.info('Adding downloads folder with files...')
        self.install_downloads()
        logger.info('Adding images folder with images...')
        self.install_images()
        logger.info('Dummy site content created.')

    def install_structure(self):
        """Setup object hierarchy."""
        # delete default Plone content
        for obj_id in ['news', 'events', 'Members']:
            if obj_id in self.context.keys():
                del self.context[obj_id]

        # TODO: create site structure with Tags, Articles etc.

    def install_downloads(self):
        """Create a downloads folder with some files."""
        pdf_filename = os.path.join(
            os.path.dirname(__file__), 'data', 'foo.pdf')
        pdf_data = file(pdf_filename, 'rb').read()
        dl = invokeFactory(self.context, 'Folder', 'Downloads')
        for i in range(10):
            download = invokeFactory(dl, 'File')
            download.setFile(pdf_data)
            download.reindexObject()

    def install_images(self):
        """Create a folder for images and populate it with random images."""
        images_container = invokeFactory(self.context, 'Folder', 'Images')
        for width, height in (
            (200, 200),
            (400, 400),
            (600, 400),
            (800, 600),
            (800, 800),
            (1024, 768)
        ):
            imagefolder_id = '%sx%s' % (width, height)
            images = invokeFactory(images_container, 'Folder', imagefolder_id)
            for i in range(10):
                img = invokeFactory(images, 'Image')
                img.setImage(random_image(width, height))
                img.reindexObject()
