from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form

# XXX: Uncomment for z3cform

from z3c.form import field

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationList, RelationChoice

from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eappi.customrss import MessageFactory as _

from plone.app.portlets.portlets import rss
from DateTime import DateTime
from DateTime.interfaces import DateTimeError


FEED_DATA = {}


class RSSFeed(rss.RSSFeed):
    def _buildItemDict(self, item):
        link = item.links[0]['href']
        picture = item.get('media_content', '')
        if len(picture) > 1:
            picture = picture[1].get('url')
        else:
            picture = ''
        itemdict = {
            'title': item.title,
            'url': link,
            'summary': item.get('description', ''),
            'media':  picture,
        }
        if hasattr(item, "updated"):
            try:
                itemdict['updated'] = DateTime(item.updated)
            except DateTimeError:
                # It's okay to drop it because in the
                # template, this is checked with
                # ``exists:``
                pass

        return itemdict


class IEappiRSS(rss.IRSSPortlet):
    """
    This portlet is subclass of rss from plone.app.porlets
    """
    pass


class Assignment(rss.Assignment):
    implements(IEappiRSS)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Renderer(rss.Renderer):

    render = ViewPageTemplateFile('templates/eappirss.pt')

    def _getFeed(self):
        """return a feed object but do not update it"""
        feed = FEED_DATA.get(self.data.url, None)
        if feed is None:
            # create it
            feed = FEED_DATA[self.data.url] = RSSFeed(self.data.url, self.data.timeout)
        return feed

    @property
    def available(self):
        return True


# XXX: z3cform
# class AddForm(z3cformhelper.AddForm):
class AddForm(rss.AddForm):

    #  XXX: z3cform
    #  fields = field.Fields(IEappiRSS)

    form_fields = form.Fields(IEappiRSS)

    label = _(u"Add Eappi RSS")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)


# XXX: z3cform
# class EditForm(z3cformhelper.EditForm):
class EditForm(rss.EditForm):

    # XXX: z3cform
    # fields = field.Fields(IEappiRSS)

    form_fields = form.Fields(IEappiRSS)

    label = _(u"Edit Eappi RSS")
    description = _(u"")
