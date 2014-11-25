#!/usr/bin/env python

from __future__ import print_function

import falcon
import json
import os
import requests
import sys

from wsgiref import simple_server


class LightsResource:

    def __init__(self):
        user = os.environ.get('ECM_USERNAME')
        password = os.environ.get('ECM_PASSWORD')
        router = os.environ.get('ECM_ROUTER')

        self.ecm_auth = (user, password)
        self.gpio_url = 'https://www.cradlepointecm.com/api/v1/remote/config/system/connector_gpio/output/?id={}'.format(router)
        self.json_header = {"Content-Type": "application/json; charset=UTF-8"}

    def get_ecm_status(self):
        r = requests.get(self.gpio_url, auth=self.ecm_auth)
        return self.return_from_ecm_response(r)

    def set_ecm_state(self, state):
        r = requests.put(self.gpio_url, headers=self.json_header,
                         data='1' if state else '0', auth=self.ecm_auth)
        return self.return_from_ecm_response(r)

    def return_from_ecm_response(self, response):
        j = json.loads(response.text)
        print(response.text)
        if j['data'][0]['success']:
            jr = {'success': True, 'status': 1 == j['data'][0]['data']}
        else:
            jr = {'success': False, 'reason': j['data'][0]['reason']}

        return json.dumps(jr)

    def set_success_status(self, resp):
        resp.status = falcon.HTTP_200
        resp.set_header('Content-Type', 'application/json')

    def put_post_handler(self, req, resp):
        try:
            input_doc = json.loads(req.stream.read())
            resp.body = self.set_ecm_state(input_doc['state'])
            self.set_success_status(resp)
        except:
            e = sys.exc_info()[1]
            raise falcon.HTTPBadRequest('bad json', str(e),
                                        headers=self.json_header)

    def on_put(self, req, resp):
        self.put_post_handler(req, resp)

    def on_post(self, req, resp):
        self.put_post_handler(req, resp)

    def on_get(self, req, resp):
        self.set_success_status(resp)
        resp.body = self.get_ecm_status()

app = falcon.API()
lights = LightsResource()
app.add_route('/lights', lights)

if __name__ == '__main__':
    server_host = '0.0.0.0'
    server_port = 5150

    httpd = simple_server.make_server(server_host, server_port, app)
    print("starting server on {}:{}".format(server_host, server_port))
    httpd.serve_forever()
