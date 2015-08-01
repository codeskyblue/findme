#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  hzsunshx
# Created: 2015-08-01 15:15

"""
findme server
"""

import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import socket


PORT = int(os.getenv("PORT", 8858))
CLEAN_INTERVAL = 10
FINDS = {}


app = Flask(__name__)

@app.route('/api/findme', methods=['POST'])
def findme_api():
    print request.remote_addr
    mac = request.form.get('mac')
    FINDS[request.remote_addr] = {
        'updated_at': datetime.now(),
        'mac': mac,
        'ifconfig': request.form.get('ifconfig'),
    }
    return jsonify({'success': True, 'message': '{} You will be found soon.'.format(mac)})

@app.route('/')
def homepage():
    for key, val in FINDS.items():
        if datetime.now() - val.get('updated_at') > timedelta(minutes=CLEAN_INTERVAL):
            try:
                del(FINDS[key])
            except: pass
    return render_template('homepage.html', finds=FINDS)

def main():
    ip = socket.gethostbyname(socket.gethostname())
    print 'Start client by --.'
    print '>>> $ SERVER=http://{ip}:{port}/api/findme python findme.py'.format(
        ip=ip, port=PORT)
    #FINDS['10.234.12.12'] = {
    #    'updated_at': datetime.now(),
    #    'ifconfig': 'haha nice',
    #    'mac': 'b8-slkj',
    #}
    app.run(host='0.0.0.0', port=PORT, debug=True)


if __name__ == '__main__':
    main()
