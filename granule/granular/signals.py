__author__ = 'beast'
from blinker import Namespace
granule_signals = Namespace()

post_save_activity = granule_signals.signal('post_save_activity')
post_save_result = granule_signals.signal('post_save_result')