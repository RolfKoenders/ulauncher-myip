import urllib2
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from netifaces import interfaces, ifaddresses, AF_INET

logger = logging.getLogger(__name__)

OPTION_IP_SHOW = "ip_show"
OPTIONVAL_ALL = "all"
OPTIONVAL_LOCAL = "local"

class MyIpExtension(Extension):

	def __init__(self):
		super(MyIpExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

	def on_event(self, event, extension):
		local_ips = ip4_addresses()
		logger.debug('Got internal ip: %s', local_ips)

		items = []
		for interface, ip in local_ips.items():
			items.append(ExtensionResultItem(icon='images/icon.png',
										name= '%s IP: %s' %  (interface,ip),
										description='Press \'enter\' to copy to clipboard.',
										on_enter=CopyToClipboardAction(ip)))

		if extension.preferences[OPTION_IP_SHOW] == OPTIONVAL_ALL:
			ip = urllib2.urlopen("http://icanhazip.com/").read()
			logger.debug('Got external ip: %s', ip)

			items = []
			items.append(ExtensionResultItem(icon='images/icon.png',
											name='External IP: %s' % ip,
											description='Press \'enter\' to copy to clipboard.',
											on_enter=CopyToClipboardAction(ip)))

		return RenderResultListAction(items)

def ip4_addresses():
    ip_list = {}
    for interface in interfaces():
        for link in ifaddresses(interface)[AF_INET]:
            ip_list[interface] = link['addr']
    return ip_list

if __name__ == '__main__':
	MyIpExtension().run()
