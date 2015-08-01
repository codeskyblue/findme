#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  hzsunshx
# Created: 2015-08-01 15:15

"""
findme server

Dependencies:
    http://flask.pocoo.org/
    https://pypi.python.org/pypi/tinydb/
"""

import os
import time
import socket
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import tinydb


PORT = int(os.getenv("PORT", 8858))
db = tinydb.TinyDB('tinydb.json')
app = Flask(__name__)

@app.route('/api/findme', methods=['POST'])
def findme_api():
    #print request.form
    remote_addr = request.remote_addr
    mac = request.form.get('mac')
    values = {
        'remote_addr': remote_addr,
        'updated_at': time.time(),
        'mac': mac,
        'ifconfig': request.form.get('ifconfig'),
    }
    if db.contains(tinydb.where('remote_addr') == remote_addr):
        db.update(values, tinydb.where('remote_addr') == remote_addr)
    else:
        db.insert(values)
    return jsonify({'success': True, 'message': '{} You will be found soon.'.format(mac)})

@app.template_filter('strftime')
def _jinja2_filter_datetime(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    dt = datetime.utcfromtimestamp(float(timestamp))
    return dt.strftime(fmt)


@app.route('/')
def homepage():
    print time.time()
    return render_template('homepage.html',
        devs=db.search(tinydb.where('updated_at') > (int(time.time()-600)))) # 10min out of date

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
