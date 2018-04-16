# -*- coding: utf-8 -*-
import json

import requests
from facebot import types

req_session = requests.session()

API_URL = "https://graph.facebook.com/v{0}/me/{1}?access_token={2}"
DEFAULT_API_VERSION = 2.6

CONNECT_TIMEOUT = 3.5
READ_TIMEOUT = 9999


def _request(token, method_name, http_method='get', params=None, files=None, base_url=API_URL):
    """Request pattern to fb API"""
    request_url = base_url.format(DEFAULT_API_VERSION, method_name, token)
    connect_timeout = CONNECT_TIMEOUT
    read_timeout = READ_TIMEOUT
    if params:
        if 'timeout' in params: read_timeout = params['timeout'] + 10
        if 'connect-timeout' in params: connect_timeout = params['connect-timeout'] + 10
    result = req_session.request(http_method, request_url, json=params, files=files,
                                 timeout=(connect_timeout, read_timeout))
    return result


def send_message(token, user_id=None, user_phone_number=None, first_name=None, last_name=None, text=None,
                 attachment=None, buttons=None, quick_replies=None, metadata=None, sender_action=None,
                 notification_type='REGULAR'):
    params = {}
    # recipient
    if user_id:
        recipient = {'id': user_id}
    elif user_phone_number:
        recipient = {'phone_number': user_phone_number}
    else:
        raise ApiException('Phone_number or id must be set', 'send_message', None)
    # regarding to API ref we need both, but in fact it don't tested
    if first_name and last_name:
        recipient['name'] = {'first_name': first_name, 'last_name': last_name}
    params['recipient'] = recipient
    # message
    if text or attachment or buttons:
        if buttons:
            payl = types.Payload(template_type="button", text=text, buttons=buttons)
            attach = types.Attachment(type="template", payload=payl)
            message = types.Message(attachment=attach)
        elif text:
            message = types.Message(text=text)
        elif attachment:
            message = types.Message(attachment=attachment)
        if quick_replies:
            message.quick_replies = quick_replies.quick_replies
        if metadata:
            message.metadata = metadata
        params['message'] = message.to_json()
    # sender_action
    elif sender_action:
        params['sender_action'] = sender_action
    else:
        raise ApiException('Text or attachment or sender_action must be set', 'send_message', None)
    # notification_type
    params['notification_type'] = notification_type
    # request
    r = _request(token, 'messages', http_method='post', params=params)
    return r.text


def send_generic(token, elements, user_id=None, user_phone_number=None):
    params = {}
    if user_id:
        recipient = {'id': user_id}
    elif user_phone_number:
        recipient = {'phone_number': user_phone_number}
    else:
        raise ApiException('Phone_number or id must be set', 'send_message', None)
    params['recipient'] = recipient
    payl = types.Payload(template_type='generic', elements=elements.elements[:10])
    attach = types.Attachment(type='template', payload=payl)
    message = types.Message(attachment=attach)
    params['message'] = message.to_json()
    r = _request(token, 'messages', http_method='post', params=params)
    return r.text


def send_list(token, elements, buttons=None, top_element_style='large', user_id=None, user_phone_number=None):
    params = {}
    if user_id:
        recipient = {'id': user_id}
    elif user_phone_number:
        recipient = {'phone_number': user_phone_number}
    else:
        raise ApiException('Phone_number or id must be set', 'send_message', None)
    params['recipient'] = recipient

    payl = types.Payload(template_type="list", top_element_style=top_element_style,
                           elements=elements.elements, buttons=buttons)
    attach = types.Attachment(type='template', payload=payl)
    message = types.Message(attachment=attach)
    params['message'] = message.to_json()
    r = _request(token, 'messages', http_method='post', params=params)
    return r.text


class ApiException(Exception):
    """Custom API exception"""

    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__("A request to the Messanger API was unsuccessful.\nMessage: {0}.\nFunction "
                                           "name: {1}.\nAPI result: {2}".format(msg, function_name, result))
        self.function_name = function_name
        self.result = result
