import os

from flask import Flask, request, Response, jsonify
from flask import render_template, send_from_directory, redirect
from flask import send_file, make_response
from url_short import app
import redis
from random import randint

r = redis.from_url(app.config['REDIS_URL'])

valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
long_url_field = 'long_url'
visits_field = 'visits'

# let angular do the routing
@app.route('/')
def basic_pages(**kwargs):
    return make_response(open('url_short/templates/index.html').read()) # TODO: change to send_file

@app.route("/loaderio-02d26f053f6e8ac2e2313a6c1d6c706f.txt", methods = ['GET'])
def loaderio_verify():
        return send_file('static/test-verify/loaderio-02d26f053f6e8ac2e2313a6c1d6c706f.txt')

@app.route("/<short_id>", methods = ['GET'])
def redirect_to_long_url(short_id):
    if r.hexists(short_id, long_url_field):
        long_url = r.hget(short_id, long_url_field)
        r.hincrby(short_id, visits_field, 1) # increment the number of visits to this url
        return redirect(long_url)
    else: # unknown short url
        return render_template('unknown.html')

@app.route("/detail", methods = ['GET'])
def detail_short_url():
    short_id = request.args.get('id', None)
    if not short_id:
        return jsonify({
                'success': False,
                'error': app.config['MSG_ID_REQ_PARAM_MISSING']
        })

    if r.hexists(short_id, long_url_field):
        long_url = r.hget(short_id, long_url_field)
        r.hincrby(short_id, visits_field, 1) # increment the number of visits to this url
        visits = r.hget(short_id, visits_field)
        return jsonify({
                'success': True,
                'long_url': long_url,
                'id': short_id,
                'short_url': request.host_url + short_id,
                'visits': visits
        })
    else: # unknown short url
        return jsonify({
                'success': False,
                'error': app.config['MSG_UNKNOWN_SHORT_URL']
        })

@app.route("/shorten", methods = ['GET'])
def shorten_url():
    long_url = request.args.get('url', None)
    if long_url:
        if long_url.startswith(request.host_url):
            return jsonify({
                    'success': False,
                    'error': app.config['MSG_ALREADY_SHORT_URL']
            })

        if r.exists(long_url): # we've seen this long_url before
            short_id = r.get(long_url)
            visits = r.hget(short_id,visits_field)
            return jsonify({
                    'success': True,
                    'long_url': long_url,
                    'id': short_id,
                    'short_url': request.host_url + short_id,
                    'visits': visits
            })
        else: # this is a new long_url
            short_id = shorten(long_url)
            while r.hexists(short_id, long_url_field): # make sure this is a unique short url
                short_id = shorten(long_url)

            r.hset(short_id, long_url_field, long_url)
            r.hset(short_id, visits_field, 0)
            r.set(long_url, short_id)

            return jsonify({
                'success': True,
                'long_url': long_url,
                'id': short_id,
                'short_url': request.host_url + short_id,
                'visits': 0
                })
    else: # useful if /shorten is called directly without a url arg
        return make_response(open('url_short/templates/index.html').read()) # TODO: change to send_file

def shorten(long_url, n=3):
    short_id = ""
    for i in range(n):
        short_id += valid_chars[randint(0,len(valid_chars)-1)]
    return short_id

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
