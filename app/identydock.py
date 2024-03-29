# -*- coding: utf-8 -*-

from flask import Flask, Response, request
import sys
import requests
import hashlib
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0 )
salt = "UNIQUE_SALT"
default_name = 'hitman'


@app.route('/', methods=['GET', 'POST'])
def mainpage():

    name = default_name
    if request.method == 'POST':
        name = request.form['name']
    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
#    hash = name_hash

    header = '<html><head><title>Identidock</title></head><body>'
    body = '''<form method= "POST">
        Hey! <input type="text" name="name" value="{}">
        <input type="submit" value="send">
        </form>
        <p> you look like:
        <img src="/monster/monster.png"/>
        '''.format( name, name_hash )
    footer = '</body></html>'

    return header + body + footer

@app.route('/monster/<name>')
def get_idention(name):

    image = cache.get(name)
    if image is None:
        print("Cache missed", flush=True)
        r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
