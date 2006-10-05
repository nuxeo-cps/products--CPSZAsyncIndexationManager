=================================
README CPSZAsyncIndexationManager
=================================
$Id$

This product patch the CPSCore IndexationManager and use zasync if
installed to do indexation asynchronously.

This is yet an experimental product do not use it in production.


Installation
------------

You need to setup a classic zeo server and client.

Create a dedicated zeo client for zasync.

Install zasync from nuxeo svn repo into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/vendor/zasync/branches/z29-nux zasync


Install nuxeo persistentqueue into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/Zope3/nuxeo.persistentqueue/trunk nuxPersistentQueue

Install the CPSZAsyncIndexationManager into your Zope instance Products::

  svn co https://svn.nuxeo.org/pub/CPS3/products/CPSZAsyncIndexationManager/trunk CPSZAsyncIndexationManager

In your zeo zasync client setup the controler and configuration::
  cp CPSZAsyncIndexationManager/zeo-zasync/bin/zasyncctl ../bin
  cp CPSZAsyncIndexationManager/zeo-zasync/etc/zasync.conf ../etc/

Edit zasyncctl and zasync.conf to setup your paths ()

All zeo clients should have the same set of Products.

Start zope: zope server, zeo client(s) then the zasync zeo using zasyncctl.

From the zmi add an 'Asynchronous Call Manager' in the root of your Zope.

Thats all.
