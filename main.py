import urllib.request, urllib.error, urllib.parse
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class MyIpExtension(Extension):

	def __init__(self):
		super(MyIpExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

	def on_event(self, event, extension):
		ip = urllib.request.urlopen("http://icanhazip.com/").read()
		logger.debug('Got external ip: %s', ip)

		items = []
		items.append(ExtensionResultItem(icon='images/icon.png',
										name='External IP: %s' % ip.decode(),
										description='Press \'enter\' to copy to clipboard.',
										on_enter=CopyToClipboardAction(ip)))

		return RenderResultListAction(items)

if __name__ == '__main__':
	MyIpExtension().run()
