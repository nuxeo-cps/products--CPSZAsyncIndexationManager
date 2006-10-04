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
# $Id: IndexationManager.py 45379 2006-05-09 15:31:23Z lregebro $
"""Manager for indexations that can be delayed using zasync.

$Id: $
"""
import logging
from Products.CPSCore.IndexationManager import IndexationManager

logger = logging.getLogger("PatchCPSCoreIndexationManager")

def process(self, ob, idxs, secu):
    """Process an object, to reindex it."""
    # The object may have been removed from its container since,
    # even if the value we have is still wrapped.
    # Re-acquire it from the root
    # FIXME: do better, by treating also indexObject/unindexObject
    root = ob.getPhysicalRoot()
    path = ob.getPhysicalPath()
    old_ob = ob
    ob = root.unrestrictedTraverse(path, None)
    if ob is None:
        logger.debug("Patched Object %r disappeared" % old_ob)
        return
    if idxs is not None:
        logger.debug("Patched reindexObject %r idxs=%r" % (ob, idxs))
        ob._reindexObject(idxs=idxs)
    if secu:
        skip_self = (idxs == [] or
                     (idxs and 'allowedRolesAndUsers' in idxs))
        logger.debug("Patched reindexObjectSecurity %r skip=%s" % (ob,
                                                                   skip_self))
        ob._reindexObjectSecurity(skip_self=skip_self)


IndexationManager.process = process
logger.info('Patching IndexationManager process to use zasync')
