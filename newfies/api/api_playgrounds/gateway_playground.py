#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#
from django.utils.translation import gettext as _
from apiplayground import APIPlayground


class GatewayAPIPlayground(APIPlayground):

    schema = {
        "title": _("gateway"),
        "base_url": "http://localhost/api/v1/",
        "resources": [
            {
                "name": "/gateway/",
                "description": _("this resource allows you to manage gateways."),
                "endpoints": [
                    {
                        "method": "GET",
                        "url": "/api/v1/gateway/",
                        "description": _("returns all gateways")
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/gateway/{gateway-id}/",
                        "description": _("returns a specific gateway")
                    },
                    {
                        "method": "POST",
                        "url": "/api/v1/gateway/",
                        "description": _("create new gateway"),
                        "parameters": [{
                                           "name": "name",
                                           "type": "string",
                                           "default": "Gateway Name"
                                       },
                                       {
                                           "name": "description",
                                           "type": "string",
                                       },
                                       {
                                           "name": "addprefix",
                                           "type": "string",
                                           "default": "91"
                                       },
                                       {
                                           "name": "removeprefix",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateways",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_codecs",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_timeouts",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_retries",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "originate_dial_string",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "failover",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "addparameter",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "maximum_call",
                                           "type": "string",
                                           "default": ""
                                       },
                                       ]
                    },
                    {
                        "method": "PUT",
                        "url": "/api/v1/gateway/{gateway-id}/",
                        "description": _("update gateway"),
                        "parameters": [{
                                           "name": "name",
                                           "type": "string"
                                       },
                                       {
                                           "name": "description",
                                           "type": "string"
                                       },
                                       {
                                           "name": "addprefix",
                                           "type": "string",
                                           "default": "91"
                                       },
                                       {
                                           "name": "removeprefix",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateways",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_codecs",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_timeouts",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "gateway_retries",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "originate_dial_string",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "failover",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "addparameter",
                                           "type": "string",
                                           "default": ""
                                       },
                                       {
                                           "name": "maximum_call",
                                           "type": "string",
                                           "default": ""
                                       },
                                       ]
                    },
                    {
                        "method": "DELETE",
                        "url": "/api/v1/gateway/{gateway-id}/",
                        "description": _("delete gateway"),
                    }
                ]
            },
            ]
    }
