# coding: utf-8

from google.appengine.ext import blobstore
from google.appengine.api import files

from flask import Flask, request, url_for, make_response, jsonify, abort

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/upload', methods=["POST"])
def upload():
    file_names = []

    for key in request.files.keys():
        file_field = request.files[key]
        file_name = files.blobstore.create(file_field.mimetype, file_field.filename)

        with files.open(file_name, 'ab') as f:
            data = file_field.read(65535)
            while data:
                f.write(data)
                data = file_field.read(65535)

        files.finalize(file_name)
        file_names.append(file_name)

    response = {}
    response['uploaded_files'] = \
    [url_for('serve', blob_key=files.blobstore.get_blob_key(file_name), _external=True)
            for file_name in file_names]

    return jsonify(response)

@app.route("/serve/<blob_key>")
def serve(blob_key):
    blob_info = blobstore.get(blob_key)
    if not blob_info:
        abort(404)

    response = make_response()
    response.headers['Content-Type'] = blob_info.content_type
    response.headers['X-AppEngine-BlobKey'] = blob_key

    #add your caching headers
    #response.headers['Expires'] = 'Sun, 19 Jul 2020 00:00:00 GMT'
    #response.headers['Cache-Control'] = 'public, max-age=315360000'
    return response

