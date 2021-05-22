# -*- coding: utf-8 -*-
"""
Created on 2018-03-21

@author: xuteng.xt
"""

import requests
import time
import hmac
import hashlib
import json
import mimetypes
import itertools
import random
import socket
import platform

P_SDK_VERSION = "lazop-sdk-python-20181207"

P_APPKEY = "app_key"
P_ACCESS_TOKEN = "access_token"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"
P_DEBUG = "debug"

P_CODE = "code"
P_TYPE = "type"
P_MESSAGE = "message"
P_REQUEST_ID = "request_id"

P_API_GATEWAY_URL_SG = "https://api.lazada.sg/rest"
P_API_GATEWAY_URL_MY = "https://api.lazada.com.my/rest"
P_API_GATEWAY_URL_VN = "https://api.lazada.vn/rest"
P_API_GATEWAY_URL_TH = "https://api.lazada.co.th/rest"
P_API_GATEWAY_URL_PH = "https://api.lazada.com.ph/rest"
P_API_GATEWAY_URL_ID = "https://api.lazada.co.id/rest"
P_API_AUTHORIZATION_URL = "https://auth.lazada.com/rest"


def sign(secret, api, parameters):
    # ===========================================================================
    # @param secret
    # @param parameters
    # ===========================================================================
    sort_dict = sorted(parameters)

    parameters_str = "%s%s" % (
        api,
        str().join("%s%s" % (key, parameters[key]) for key in sort_dict),
    )

    h = hmac.new(
        secret.encode(encoding="utf-8"),
        parameters_str.encode(encoding="utf-8"),
        digestmod=hashlib.sha256,
    )

    return h.hexdigest().upper()


class LazopRequest(object):
    def __init__(self, api_pame, http_method="POST"):
        self._api_params = {}
        self._file_params = {}
        self._api_pame = api_pame
        self._http_method = http_method

    def add_api_param(self, key, value):
        self._api_params[key] = value

    def add_file_param(self, key, value):
        self._file_params[key] = value


class LazopResponse(object):
    def __init__(self):
        self.type = None
        self.code = None
        self.message = None
        self.request_id = None
        self.body = None

    def __str__(self, *args, **kwargs):
        sb = (
            "type="
            + mixStr(self.type)
            + " code="
            + mixStr(self.code)
            + " message="
            + mixStr(self.message)
            + " requestId="
            + mixStr(self.request_id)
        )
        return sb


class LazopClient(object):
    def __init__(self, server_url, app_key, app_secret, timeout=30):
        self._server_url = server_url
        self._app_key = app_key
        self._app_secret = app_secret
        self._timeout = timeout

    def execute(self, request, access_token=None):

        sys_parameters = {
            P_APPKEY: self._app_key,
            P_SIGN_METHOD: "sha256",
            P_TIMESTAMP: str(int(round(time.time()))) + "000",
            P_PARTNER_ID: P_SDK_VERSION,
        }

        if access_token:
            sys_parameters[P_ACCESS_TOKEN] = access_token

        application_parameter = request._api_params

        sign_parameter = sys_parameters.copy()
        sign_parameter.update(application_parameter)

        sign_parameter[P_SIGN] = sign(
            self._app_secret, request._api_pame, sign_parameter
        )

        api_url = "%s%s" % (self._server_url, request._api_pame)

        full_url = api_url + "?"
        for key in sign_parameter:
            full_url += key + "=" + str(sign_parameter[key]) + "&"
        full_url = full_url[0:-1]

        try:
            if request._http_method == "POST" or len(request._file_params) != 0:
                r = requests.post(
                    api_url,
                    sign_parameter,
                    files=request._file_params,
                    timeout=self._timeout,
                )
            else:
                r = requests.get(api_url, sign_parameter, timeout=self._timeout)
        except Exception as err:
            raise err

        return r.json()
