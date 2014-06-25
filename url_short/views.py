import os

from flask import Flask, request, Response, jsonify
from flask import render_template, send_from_directory
from flask import send_file, make_response
from url_short import app
import redis
from random import randint

r = redis.from_url(app.config['REDISTOGO_URL'])
valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
long_url_field = 'short_url'
visits_field = 'visits'

# let angular do the routing
@app.route('/')
def basic_pages(**kwargs):
    return make_response(open('url_short/templates/index.html').read()) # TODO: change to send_file

@app.route("/<short_url>", methods = ['GET'])
def lengthen_url(short_url):
    if r.hexists(short_url, long_url_field):
        long_url = r.hget(short_url, long_url_field)
        r.hincrby(short_url, visits_field, 1) # increment the number of visits to this url
        visits = r.hget(short_url, visits_field)
        return jsonify({
                'success': True,
                'long_url': long_url,
                'short_url': short_url,
                'visits': visits
            })
    else:
        return jsonify({
                'success': False
            })

@app.route("/shorten", methods = ['GET'])
def shorten_url():
    long_url = request.args.get('url', None)
    if long_url:
        if r.exists(long_url): # we've seen this long_url before
            short_url = r.get(long_url)
            visits = r.hget(short_url,visits_field)
            return jsonify({
                    'success': True,
                    'long_url': long_url,
                    'short_url': short_url,
                    'visits': visits
                })
        else: # this is a new long_url
            short_url = shorten(long_url)
            while r.hexists(short_url, long_url_field): # make sure this is a unique short url
                short_url = shorten(long_url)

            r.hset(short_url, long_url_field, long_url)
            r.hset(short_url, visits_field, 0)
            r.set(long_url, short_url)

            return jsonify({
                'success': True,
                'long_url': long_url,
                'short_url': short_url,
                'visits': 0
                })
    else: # useful if /shorten is called directly without a url arg
        return make_response(open('url_short/templates/index.html').read()) # TODO: change to send_file

def shorten(long_url, n=3):
    short_url = ""
    for i in range(n):
        short_url += valid_chars[randint(0,len(valid_chars)-1)]
    return short_url

# special file handlers and error handlers
#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
