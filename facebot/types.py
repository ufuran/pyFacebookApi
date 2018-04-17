# -*- coding: utf-8 -*-

try:
    import ujson as json
except ImportError:
    import json

import six


class JsonD:
    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def __str__(self):
        d = {}
        for x, y in six.iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return six.text_type(d)


class Message(JsonD):
    def __init__(self, text=None, attachment=None, quick_replies=None, metadata=None):
        if text is not None:
            self.text = text
        self.attachment = attachment
        self.metadata = metadata
        if quick_replies:
            self.quick_replies = quick_replies.quick_replies


class QuickReplies(JsonD):
    def __init__(self):
        self.quick_replies = []

    def add(self, quick_replie):
        self.quick_replies.append(quick_replie)


class QuickReplie(JsonD):
    def __init__(self, content_type='text', title=None, payload=None, image_url=None):
        self.content_type = content_type
        self.image_url = image_url
        if self.content_type == 'text':
            if title:
                self.title = title
            else:
                raise Exception("Error in QuickReplie")
            self.payload = payload
            self.image_url = image_url
        elif self.content_type != 'location':
            raise Exception("content_type not in ['location', 'text']")


class Attachment(JsonD):
    def __init__(self, _type, payload):
        self.type = _type
        self.payload = payload


class Payload(JsonD):
    def __init__(self, template_type, text=None, buttons=None, elements=None, top_element_style='large'):
        self.template_type = template_type
        if self.template_type == 'button':
            if text is not None:
                self.text = text
            self.buttons = buttons.buttons
        elif self.template_type == 'generic':
            self.elements = elements
        elif self.template_type == 'list':
            self.elements = elements
            self.top_element_style = top_element_style
            if buttons is not None:
                self.buttons = buttons.buttons[:1]
        else:
            raise Exception("Error in Payload class")


class Elements(JsonD):
    def __init__(self):
        self.elements = []

    def add(self, element):
        if type(element) is Element:
            self.elements.append(element)
        else:
            raise Exception("Element must be class Element")

class Element(JsonD):
    def __init__(self, title, item_url=None, default_action=None, image_url=None, subtitle=None, buttons=None):
        self.title = title
        self.item_url = item_url
        if item_url is None:
            self.default_action = default_action #url button
        self.image_url = image_url
        self.subtitle = subtitle
        if buttons is not None:
            self.buttons = buttons.buttons


class Buttons(JsonD):
    def __init__(self):
        self.buttons = []

    def add(self, button):
        if type(button) is UrlButton or type(button) is PostbackButton:
            self.buttons.append(button)
        else:
            raise Exception("Button must be class UrlButton or PostbackButton")


class UrlButton(JsonD):
    def __init__(self, url, title=None, _type="web_url", webview_height_ratio="full", messenger_extensions=False,
                 fallback_url=None, webview_share_button=None):
        self.type = _type
        self.title = title
        self.url = url
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions
        self.fallback_url = fallback_url
        self.webview_share_button = webview_share_button


class PostbackButton(JsonD):
    def __init__(self, payload, title=None, _type="postback"):
        self.type = _type
        self.title = title
        self.payload = payload
