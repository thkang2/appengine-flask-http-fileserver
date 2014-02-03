# coding: utf-8

from google.appengine.ext import blobstore
from google.appengine.api import files

from flask import Flask, request, url_for, make_response, jsonify, abort, Response

app = Flask(__name__)


@app.after_request
def after_request(response):
    """ allows cross-domain uploads via ajax. """
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
    

@app.route("/serve/<blob_key>", methods=["GET"])
def serve(blob_key):
    blob_info = blobstore.get(blob_key)
    if not blob_info:
        #the blob does not exist. return 404 error.
        abort(404)

    if request.headers.get('If-None-Match'):
        #the client has an Etag of previously served content.
        #the idea of blobstore, at least in current project, is that uploaded blobs may be deleted but never modified. so, tell the client to fetch it from the cache.
        return Response(status=304)

    response = make_response()
    response.headers['Content-Type'] = blob_info.content_type
    #a very long max-age (10 yrs)
    response.headers['Cache-Control'] = 'public, max-age=315360000'

    #very basic caching based on etags; etag == blob_key
    response.headers['ETag'] = '"%s"' %blob_key

    #this line tells google app engine server to fill the body of this response with the actual blob content.
    response.headers['X-AppEngine-BlobKey'] = blob_key
    
    return response
