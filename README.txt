=================================
README CPSZAsyncIndexationManager
=================================
$Id$

This product patch the CPSCore IndexationManager and use zasync if
installed to do indexation asynchronously.


Installation
------------

You need to setup a classic zeo server and client.

Create a dedicated zeo client for zasync.

Install zasync from nuxeo svn repo into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/vendor/zasync/branches/z29-nux zasync


Install nuxeo persistentqueue into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/Zope3/nuxeo.persistentqueue/trunk nuxPersistantQueue

Install the CPSZAsyncIndexationManager into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/CPS3/products/CPSZAsyncIndexationManager/trunk CPSZAsyncIndexationManager


All zeo clients should have the same set of Products.

Start all your zss and zeos.

From the zmi add an 'Asynchronous Call Manager' in the root of your Zope.

Thats all.
