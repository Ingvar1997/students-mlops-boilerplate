import time

import redis
from flask import Flask, request, jsonify

from helpers import convert_base64_im_to_np, convert_np_im_to_base64

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/v1.0/image/run-segmentation', methods=['POST'])
def run_segmentation():
    if not request.json or not 'im_base64' in request.json:
        return jsonify({'error_msg': 'No image provided'}, 400)
    request_json = request.json  
    im_base64 = request_json['im_base64']
    im_np = convert_base64_im_to_np(im_base64)

    # DO SOME MANIPULATIONS HERE

    transformed_image = convert_np_im_to_base64(im_np)
    return jsonify({'im_base64': transformed_image}), 200
