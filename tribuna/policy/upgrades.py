from plone import api

import logging
logger = logging.getLogger(__name__)


def fix_annotation_ids(context):
    """Set annotation UID as the id for all annotations (we need to have
    globally unique annotation ids for the @@articles view).
    """
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='tribuna.annotator.annotation')

    for brain in brains:
        annotation = brain.getObject()
        api.content.rename(
            obj=annotation, new_id=annotation.UID(), safe_id=True)

    logger.info('Changed annotation ids to UIDs.')