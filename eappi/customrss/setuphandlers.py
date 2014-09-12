from collective.grok import gs
from eappi.customrss import MessageFactory as _

@gs.importstep(
    name=u'eappi.customrss', 
    title=_('eappi.customrss import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('eappi.customrss.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
