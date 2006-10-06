# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$
"""Manager for indexations that can be delayed using zasync.

$Id$
"""
import logging

from Products.CMFCore.utils import getToolByName
from Products.CPSCore.IndexationManager import IndexationManager
from Products.CPSCore.ProxyBase import ProxyBase

logger = logging.getLogger("PatchCPSCoreIndexationManager")

# Patching ProxyBase
ProxyBase.do_reindexObject = ProxyBase._reindexObject
ProxyBase.do_reindexObjectSecurity = ProxyBase._reindexObjectSecurity
logger.info('Patching ProxyBase to add do_reindexObject* methods.')


def getZAsyncUsage(portal):
    """Return
    None       if zasync is not installed,
    'security' if zasync is used only for reindexObjectSecurity,
    'all'      use zasync for reindexObject and reindexObjectSecurity.
    """
    root = portal.getPhysicalRoot()
    if 'asynchronous_call_manager' not in root.objectIds():
        return None
    async_type = getattr(portal, 'use_async_index_manager', None)
    if not async_type:
        return None
    if 'security' in str(async_type.lower()):
        return 'security'
    return 'all'

# Patching IndexationManager
def process(self, ob, idxs, secu):
    """Process an object, to reindex it.

    Patched to it asynchronously if zasync is installed."""
    # The object may have been removed from its container since,
    # even if the value we have is still wrapped.
    # Re-acquire it from the root
    # FIXME: do better, by treating also indexObject/unindexObject

    root = ob.getPhysicalRoot()
    path = ob.getPhysicalPath()
    old_ob = ob
    ob = root.unrestrictedTraverse(path, None)
    if ob is None:
        logger.debug("Object %r disappeared" % old_ob)
        return
    utool = getToolByName(ob, 'portal_url')
    portal = utool.getPortalObject()
    async_usage = getZAsyncUsage(portal)

    if idxs is not None and (not async_usage or async_usage != 'all'):
        logger.debug("reindexObject %r idxs=%r" % (ob, idxs))
        ob._reindexObject(idxs=idxs)
    if not async_usage and secu:
        skip_self = (idxs == [] or
                     (idxs and 'allowedRolesAndUsers' in idxs))
        logger.debug("reindexObjectSecurity %r skip=%s" % (ob, skip_self))
        ob._reindexObjectSecurity(skip_self=skip_self)
    if not async_usage:
        return

    # The indexation later tries to index the changed language revision.
    # For this it normally uses the AcceptLanguage method on the
    # request, but it doesn't exist in zasyncs request. We can avoid
    # this by adding a _cps_switch_language setting, basically telling
    # the proxy when accessed by zasync to switch language to the one
    # used by the real access.
    rpath = utool.getRelativeUrl(ob)
    lang = None
    if ob.REQUEST.has_key('_cps_switch_language'):
        # If there is a switch for this proxy, use that one.
        rpath2, lang2 = ob.REQUEST._cps_switch_language
        if rpath == rpath2:
            lang = lang2
    if lang and ob.REQUEST.has_key('AcceptLanguage'):
        # Otherwise find the current langauge match, and use it.
        lang = ob.REQUEST.AcceptLanguage.select_language(
            ob._language_revs.keys())
    if lang is None:
        # Couldn't find any language, use proxy default.
        lang = ob._default_language
    if idxs is not None and async_usage == 'all':
        logger.debug("zasync call reindexObject %r idxs=%r" % (ob, idxs))
        root.asynchronous_call_manager.putCall(
            'zope_exec', path, {'idxs': idxs,
                                '_cps_switch_language': (rpath, lang),},
            'python: here.do_reindexObject(idxs=request.idxs)'
            )
    if secu:
        skip_self = (idxs == [] or
                     (idxs and 'allowedRolesAndUsers' in idxs))
        logger.debug("zasync reindexObjectSecurity %r skip=%s" % (ob,
                                                                  skip_self))
        root.asynchronous_call_manager.putCall(
            'zope_exec', path, {'_cps_switch_language': (rpath, lang)},
            'python: here.do_reindexObjectSecurity(skip_self=%s)' % skip_self
            )


IndexationManager.process = process
logger.info('Patching IndexationManager process to use zasync')
