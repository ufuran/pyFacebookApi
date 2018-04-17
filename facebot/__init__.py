# -*- coding: utf-8 -*-

import threading
try:
    import ujson as json
except ImportError:
    import json
from facebot import apihelper


class RunThread(threading.Thread):
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        threading.Thread.__init__(self)

    def run(self):
        self.target(*self.args)


class bot:
    def __init__(self, ACCESS_TOKEN, VERIFY_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.VERIFY_TOKEN = VERIFY_TOKEN
        self.handler = []

    def message_handler(self, content_type, func=None, **kwargs):
        def decorate(handler):
            self.handler.append({'handler': handler, 'func': func, 'content_type': content_type, 'outher': kwargs})
            return handler

        return decorate

    def process_new_message(self, message):
        for hand in self.handler:
            if message['content_type'] == hand['content_type'] and (hand['func'] is None or hand['func'](message)):
                process_handel = RunThread(hand['handler'], message)
                process_handel.start()
                break

    def check_webhook(self, hub):
        if hub == self.VERIFY_TOKEN:
            return True
        else:
            return False

    def received_new_message(self, updates):
        updates = json.loads(updates)
        if 'entry' in updates and type(updates["entry"]) == list:
            for entry in updates["entry"]:
                if 'messaging' in entry and type(entry['messaging']) == list:
                    for message in entry['messaging']:
                        if "message" in message and 'quick_reply' in message['message']:
                            message['content_type'] = "quick_reply"
                        elif "message" in message and 'attachments' in message['message']:
                            message['content_type'] = 'attachments'
                        elif "message" in message and 'text' in message['message']:
                            message['content_type'] = 'text'
                        else:
                            if 'postback' in message:
                                message['content_type'] = 'postback'
                            else:
                                message['content_type'] = 'other'
                        self.process_new_message(message)

    def send_message(self, **kwargs):
        return apihelper.send_message(self.ACCESS_TOKEN, **kwargs)

    def send_generic(self, **kwargs):
        return apihelper.send_generic(self.ACCESS_TOKEN, **kwargs)

    def send_list(self, **kwargs):
        return apihelper.send_list(self.ACCESS_TOKEN, **kwargs)
